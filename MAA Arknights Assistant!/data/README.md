# 一图流干员数据

- 获取日期：2026-10-10（北京时间）。
- 来源：明日方舟一图流第三方 OpenAPI。
- 返回状态：HTTP 200，业务状态 `code: 200`，`msg: 操作成功`。
- 干员数量：225；已检查 ID 无重复、必要字段齐全，且保存后可以重新解析。
- 数据是接口返回时的快照。接口没有提供这份数据的游戏内同步时间，不能据此判断是否与当前游戏账号实时一致。

## 本地文件

- `operators-2026-10-10.raw.json`：原始响应正文，保留 `code`、`msg`、`data`。
- `operators-2026-10-10.json`：格式化后的干员数组，内容来自原始响应的 `data`，便于阅读和后续处理。

原始响应文件 SHA-256：

```text
c7ac3b316872c78b0c403dc3cac68ec123dd823a11d24e8fe2f38d94a5f94117
```

## 已核实的调用方法

依据一图流官方页面及其前端实现：

- 测试页面：https://ark.yituliu.cn/dev/open-api-test
- 前端实现：https://ark.yituliu.cn/assets/open-api-test-CEIqcfS3.js
- 请求方法：`GET`
- 请求地址：`https://backend.yituliu.cn/open-api/operator/info`
- 请求头：`Authorization: <你的只读 API 密钥>`，直接填写密钥，不加 `Bearer` 前缀。
- 无请求正文。

密钥未保存到本目录的文件中。

## 数据字段

以下字段保留接口原值，不转换等级或潜能的编号规则：

| 字段 | 内容 |
| --- | --- |
| `id` | 干员 ID |
| `level` | 当前等级 |
| `evolvePhase` | 精英化阶段 |
| `mainSkillLevel` | 通用技能等级 |
| `skills` | 技能数组，每项包含 `id`、`level` |
| `equips` | 模组数组，每项包含 `id`、`type`、`level` |
| `potentialRank` | 潜能数值 |

此接口返回的数据不包含中文干员名、稀有度或信赖值，本地文件未补造这些字段。
