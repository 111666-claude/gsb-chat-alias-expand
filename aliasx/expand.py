"""按句子逐词展开别名。"""


def expand(index, line, req_id, ledger, counter):
    if req_id in ledger:
        out = dict(ledger[req_id])
        out["status"] = "replay"
        return out
    blocked = set(index.get("blocked", []))
    tokens = []
    for raw in line.split():
        if not raw.startswith("/") or len(raw) == 1:
            tokens.append({"raw": raw, "status": "literal", "command": None})
            continue
        hit = _match(index, raw[1:], counter)
        if hit is None:
            tokens.append({"raw": raw, "status": "unknown", "command": None})
        elif hit[0] in blocked:
            tokens.append({"raw": raw, "status": "blocked", "command": None})
        else:
            tokens.append({"raw": raw, "status": "expanded", "command": hit[1]})
    expanded = " ".join(t["command"] if t["command"] is not None else t["raw"] for t in tokens)
    out = {
        "req_id": req_id,
        "status": "ok",
        "line": line,
        "expanded": expanded,
        "tokens": tokens,
        "scanned": counter.scanned,
    }
    ledger[req_id] = out
    return out


def _match(index, name, counter):
    node = index["trie"]
    hit = None
    for depth, ch in enumerate(name, 1):
        node = node.get(ch)
        if node is None:
            break
        command = node.get("\0")
        if command is not None:
            counter.scanned += 1
            hit = (name[:depth], command)
    return hit
