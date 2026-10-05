"""把别名表编成可以逐字符走的索引。"""


def build_index(aliases, overrides, player, blocked):
    """合并各层并建索引。"""
    effective = dict(aliases)
    returns = {"effective": effective, "blocked": [], "trie": _trie(effective)}
    return returns


def _trie(effective):
    root = {}
    for alias, command in effective.items():
        node = root
        for ch in alias:
            node = node.setdefault(ch, {})
        node["\0"] = command
    return root
