"""把别名表编成可以逐字符走的索引。"""


def build_index(aliases, overrides, player, blocked):
    """合并各层并建索引。"""
    effective = dict(aliases)
    if player and isinstance(overrides, dict):
        effective.update(overrides.get(player, {}))
    if isinstance(blocked, dict):
        blocked = blocked.get(player, []) if player else []
    blocked = list(blocked or [])
    return {"effective": effective, "blocked": blocked, "trie": _trie(effective)}


def _trie(effective):
    root = {}
    for alias, command in effective.items():
        node = root
        for ch in alias:
            node = node.setdefault(ch, {})
        node["\0"] = command
    return root
