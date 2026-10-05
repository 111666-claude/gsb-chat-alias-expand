"""命令行入口。"""

import argparse
import json

from . import build, expand


class Counter:
    def __init__(self):
        self.scanned = 0


def _load(path, default=None):
    if not path:
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _dump(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="aliasx")
    ap.add_argument("--sample", choices=["longest", "override", "blocked", "replay", "work"])
    sub = ap.add_subparsers(dest="cmd")

    bd = sub.add_parser("build")
    bd.add_argument("--aliases", required=True)
    bd.add_argument("--overrides")
    bd.add_argument("--player")
    bd.add_argument("--blocked")
    bd.add_argument("--out", required=True)

    ex = sub.add_parser("expand")
    ex.add_argument("--index", required=True)
    ex.add_argument("--line", required=True)
    ex.add_argument("--req-id", required=True)
    ex.add_argument("--ledger")

    args = ap.parse_args(argv)
    if args.sample:
        from . import samples
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    if args.cmd == "build":
        overrides = _load(args.overrides, {})
        blocked = _load(args.blocked, {})
        if args.player:
            blocked = blocked.get(args.player, []) if isinstance(blocked, dict) else blocked
        index = build.build_index(_load(args.aliases, {}), overrides, args.player, blocked)
        _dump(args.out, index)
        print(json.dumps({"player": args.player, "aliases": len(index["effective"])}, ensure_ascii=False))
        return 0

    index = _load(args.index, {})
    ledger = _load(args.ledger, {}) or {}
    out = expand.expand(index, args.line, args.req_id, ledger, Counter())
    if args.ledger:
        _dump(args.ledger, ledger)
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
