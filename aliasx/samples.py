"""固定场景，用来复现题面里的锚点。"""

import json

from . import build, expand


class Counter:
    def __init__(self):
        self.scanned = 0


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _index(aliases, overrides=None, player=None, blocked=None):
    return build.build_index(aliases, overrides or {}, player, blocked or [])


def run(name):
    if name == "longest":
        index = _index({"g": "guild", "gc": "guild-chat", "w": "whisper"})
        out = expand.expand(index, "/gc hi", "long-1", {}, Counter())
        _line({"status": out["status"], "expanded": out["expanded"]})
        return 0
    if name == "override":
        index = _index({"w": "whisper"}, {"p1": {"w": "whisper-pm"}}, "p1")
        out = expand.expand(index, "/w bob", "over-1", {}, Counter())
        _line({"status": out["status"], "expanded": out["expanded"]})
        return 0
    if name == "blocked":
        index = _index({"gc": "guild-chat"}, None, None, ["gc"])
        out = expand.expand(index, "/gc hi", "block-1", {}, Counter())
        _line({"status": out["status"], "expanded": out["expanded"],
               "token_status": out["tokens"][0]["status"]})
        return 0
    if name == "replay":
        index = _index({"tp": "teleport"})
        ledger = {}
        first = expand.expand(index, "/tp a", "rep-1", ledger, Counter())
        second = expand.expand(index, "/tp b", "rep-1", ledger, Counter())
        _line({"status": first["status"], "expanded": first["expanded"], "ledger": len(ledger)})
        _line({"status": second["status"], "expanded": second["expanded"], "ledger": len(ledger)})
        return 0
    if name == "work":
        aliases = {}
        for i in range(120):
            aliases["g%03d" % i] = "cmd-%03d" % i
        index = _index(aliases)
        counter = Counter()
        for i in range(2000):
            expand.expand(index, "/g119 x", "w-%d" % i, {}, counter)
        _line({"tokens": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
