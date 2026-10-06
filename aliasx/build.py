"""把别名表编成可以逐字符走的索引。"""


def build_index(aliases, overrides, player, blocked):
    """合并各层并建索引。"""
    effective = dict(aliases)
    if player and overrides:
        effective.update(overrides.get(player, {}))
    return {
        "effective": effective,
        "blocked": list(blocked or []),
        "trie": _trie(effective),
    }


def _trie(effective):
    root = {}
    for alias, command in effective.items():
        node = root
        for ch in alias:
            node = node.setdefault(ch, {})
        node["\0"] = command
    return root
