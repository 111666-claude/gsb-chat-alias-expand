"""按句子逐词展开别名。"""


def expand(index, line, req_id, ledger, counter):
    tokens = []
    for raw in line.split():
        if not raw.startswith("/") or len(raw) == 1:
            tokens.append({"raw": raw, "status": "literal", "command": None})
            continue
        command = _match(index, raw[1:], counter)
        if command is None:
            tokens.append({"raw": raw, "status": "unknown", "command": None})
        else:
            tokens.append({"raw": raw, "status": "expanded", "command": command})
    expanded = " ".join(t["command"] if t["command"] else t["raw"] for t in tokens)
    ledger[req_id] = {"expanded": expanded}
    return {
        "req_id": req_id,
        "status": "ok",
        "line": line,
        "expanded": expanded,
        "tokens": tokens,
        "scanned": counter.scanned,
    }


def _match(index, name, counter):
    for alias, command in index["effective"].items():
        counter.scanned += 1
        if name.startswith(alias):
            return command
    return None
