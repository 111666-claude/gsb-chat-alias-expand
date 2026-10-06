"""按句子逐词展开别名。"""


def expand(index, line, req_id, ledger, counter):
    if req_id in ledger:
        cached = ledger[req_id]
        return {
            "req_id": req_id,
            "status": "replay",
            "line": cached.get("line", line),
            "expanded": cached["expanded"],
            "tokens": cached.get("tokens", []),
            "scanned": counter.scanned,
        }

    blocked = set(index.get("blocked", []))
    tokens = []
    for raw in line.split():
        if not raw.startswith("/") or len(raw) == 1:
            tokens.append({"raw": raw, "status": "literal", "command": None})
            continue
        alias, command = _match(index, raw[1:], counter)
        if command is None:
            tokens.append({"raw": raw, "status": "unknown", "command": None})
        elif alias in blocked:
            tokens.append({"raw": raw, "status": "blocked", "command": None})
        else:
            tokens.append({"raw": raw, "status": "expanded", "command": command})
    expanded = " ".join(t["command"] if t["command"] else t["raw"] for t in tokens)
    ledger[req_id] = {"line": line, "expanded": expanded, "tokens": tokens}
    return {
        "req_id": req_id,
        "status": "ok",
        "line": line,
        "expanded": expanded,
        "tokens": tokens,
        "scanned": counter.scanned,
    }


def _match(index, name, counter):
    effective = index["effective"]
    for end in range(len(name), 0, -1):
        counter.scanned += 1
        alias = name[:end]
        if alias in effective:
            return alias, effective[alias]
    return None, None
