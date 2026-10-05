# chat-alias-expand

聊天指令别名展开：先把别名表编成索引，再拿索引逐条展开。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m aliasx build  --aliases a.json --overrides o.json --player p1 --blocked b.json --out index.json
python3 -m aliasx expand --index index.json --line "/gc hi" --req-id r1 --ledger ledger.json
python3 -m aliasx --sample=longest|override|blocked|replay|work
```

`--aliases` 是 `{"别名": "规范指令"}`，`--overrides` 是 `{"玩家": {"别名": "规范指令"}}`，
`--blocked` 是 `{"玩家": ["别名", ...]}`。

## 口径

- **最长前缀**：一个 `/` 开头的词，取能作为它前缀的、最长的那个别名来展开。
- **覆盖层**：该玩家的覆盖表优先于全局别名表，覆盖层里的条目替换同名的全局条目。
- **屏蔽层**：该玩家被屏蔽的别名不展开，原样保留。
- **幂等**：同一个 `req_id` 只展开一次，重复请求返回首次结果，台账不再追加。
- 非 `/` 开头的词原样透传；匹配不到任何别名的 `/` 词标记为 `unknown` 并原样保留。

## 不变量

- 展开结果的词数与原句一致。
- 同一个 `req_id` 无论请求几次，`expanded` 都一样。
- `scanned` 不随别名表长度放大：两千个词展开时不超过 6000。

## 输出契约

每次展开打印一行 JSON：`req_id`、`status`（`ok` / `replay`）、`line`、`expanded`、
`tokens`（每项含 `raw`、`status`（`expanded` / `blocked` / `unknown` / `literal`）、`command`）、`scanned`。

`--sample=work` 只打印 `{"tokens": N, "scanned": N}`。
