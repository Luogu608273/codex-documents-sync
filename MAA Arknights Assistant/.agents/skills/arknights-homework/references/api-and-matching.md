# 已核实的接口和匹配规则

核实日期：2026-10-10。接口实测与官方源码交叉核对；网页按钮行为来自源码，本次没有操作浏览器导入，也没有实战运行作业。

## 只读接口

PRTS Plus 后端基址：`https://prts.maa.plus`。以下三个查询无需登录，本次均成功返回 `status_code: 200`：

| 用途 | 方法与路径 | 说明 |
| --- | --- | --- |
| 关卡目录 | `GET /arknights/level` | `data` 是数组，含 `stage_id`、`level_id`、`cat_one`、`cat_two`、`cat_three`、`name` |
| 作业检索 | `GET /copilot/query` | `data` 是分页对象，含 `has_next`、`page`、`total`、`data` |
| 单个作业 | `GET /copilot/get/{id}` | `data` 是作业元数据，`content` 是 JSON 字符串，须再解析一次 |

只调用这些已确认的读取路径。不能根据 GET 方法判断其他接口只读，例如源码里的 `/copilot/status` 是修改操作。

查询示例：

```text
https://prts.maa.plus/copilot/query?levelKeyword=main_01-07&page=1&limit=2&orderBy=hot&desc=true
https://prts.maa.plus/copilot/get/22311
```

实测首个请求返回 1-7 作业，第二个返回“1-7 稀音 单人 61s 速刷 信赖 无专”；作业可能后续更新，不把示例当固定推荐。

常用查询参数：

- `levelKeyword`：内部 `stage_id`；例如 `main_01-07`。
- `document`：标题／说明关键词，是文字搜索，不能当精确关卡筛选。实测 `document=1-7` 包含其他关卡作业。
- `page`：从 1 开始；`limit`：最多 50。
- `orderBy`：前端定义 `hot`、`views`、`id`；`desc=true` 为倒序。
- `operator`：前端把包含干员和排除干员拼成逗号串，排除名前加 `~`。这不是整份 Box 的匹配接口。
- `type`：前端支持作业类型筛选。当前另有 VIDEO 作业；不能把视频记录当可运行的 MAA JSON 作业。

线上前端客户端使用 `levelKeyword`、`orderBy`，后端 HEAD 源码也出现 `level_keyword`、`order_by` 绑定；本次使用两组参数配合 `main_01-07` 都得到对应关卡。优先使用上述已测示例，不推断所有别名均永久兼容。

**关键陷阱**：`levelKeyword=1-7` 和 `level_keyword=1-7` 实测都返回无关关卡，HTTP 和业务码仍为 200。必须先映射内部 ID，再核对返回内容。

## 关卡与分页

- `cat_three` 是显示编号，`cat_two` 是活动／章节；显示编号可能重复。
- `stage_id` 是唯一标识。`level_id` 是资源路径，不能和显示编号混用。
- `#f#` 后缀在站点逻辑中表示突袭／困难；引航者还区分 `bossrush_`、`bossrush_tm`。作业内容另有 `difficulty` 位标志：1 普通、2 困难、3 两者，未填则未知。不要擅自认定未填就是普通。
- API 的关卡查询可能返回相关模式，正文还可能有额外说明；必须再核对 `content.stage_name` 和难度。
- 根据 `has_next` 决定是否还有分页，按作业 ID 去重。`total` 是服务端检索总量，不是已匹配数量。
- 一图流匹配器源码默认每页 50、一次最多 6 页；PRTS Plus 的空匹配列表也只会自动补有限页数。不得把局部分页当全库搜索。

## 一图流数据及名称映射

```text
GET https://backend.yituliu.cn/open-api/operator/info
Authorization: <只读密钥原值，不加 Bearer>
```

完整响应：`{code: 200, msg: ..., data: [...]}`。PRTS Plus 本地导入兼容完整响应或纯 `data` 数组。

官方干员目录（公开 JSON）：

`https://raw.githubusercontent.com/ZOOT-Plus/zoot-plus-frontend/main/src/models/generated/operators.json`

使用其中 `OPERATORS` 的 `id`、`name`、`rarity`、`prof`、`modules` 映射。目录包含召唤物等记录，不把目录长度当干员持有数。记录目录来源和核对时间；新干员 ID 不在目录时应刷新或单独查证。

| 一图流字段 | 用途 |
| --- | --- |
| `id` | 映射干员名；保留 ID 和职业以区分重名／形态 |
| `evolvePhase` | 精英化阶段 0／1／2 |
| `level` | 当前精英化阶段内等级 |
| `mainSkillLevel` | 通用技能等级 |
| `skills[i].level` | 第 i+1 个技能专精等级 0～3；原生前端按数组顺序读取 |
| `equips[].type`、`level` | 模组类型与等级；0 级不算已解锁 |
| `potentialRank` | 原样保留；本次未核实其编号换算，不能自行加一或减一 |

干员阵容匹配不能只拿名字求子集。原生前端通过名字建立 Map，重名形态可能覆盖；有 `role` 或同名多个 ID 时须人工复核。

### 本项目已发现的目录差异

2026-10-10 实际比对本地 225 条记录与官方 main 分支目录：223 条 ID 可映射，以下两条不能映射；原生 `normalizeYituliuOwnedOperators` 遇到未知 ID 会跳过，所以预计导入数量为 223。该数量来自数据和源码核对，没有声称已在浏览器里实测导入。

| 一图流 ID | 一图流线上资料中的名称 | 处理 |
| --- | --- | --- |
| `char_1001_amiya2` | 阿米娅（近卫） | 保留独立记录，按近卫技能与模组复核 |
| `char_1037_amiya3` | 阿米娅（医疗） | 保留独立记录，按医疗技能与模组复核 |

一图流主页面构建资源 `https://ark.yituliu.cn/assets/main-BUYSSUly.js` 中已核对上述 ID 与名称。PRTS Plus 目录当前只包含 `char_002_amiya`（术师）。不要为了凑导入数量把两个 ID 改成术师 ID，或把技能专精／模组覆盖到术师记录上。若作业只写“阿米娅”而没有区分形态，须根据 `role`、作者说明和使用技能确认；同一角色的不同升变形态不能同时编队。[PRTS 近卫阿米娅资料](https://prts.wiki/w/阿米娅(近卫))说明不同职业共用经验／精英等级等，专精不共用。

## 原生筛选逻辑与必要复核

PRTS Plus 在浏览器内对已取得作业执行匹配，没有把用户一图流密钥附在作业查询中。已验证的源码入口是 `src/models/operatorMatcher.ts`。

1. 固定 `opers` 每人一槽；每个 `groups` 替代组一槽，组内任意一个持有且条件达标就判该组达标。
2. 普通技能要求 `skill_level <= 7` 与 `mainSkillLevel` 比较。8／9／10 分别对应指定技能专一／二／三。
3. 精英化和等级用累计进度比较，不单独比较等级数字。例如精二 1 级高于精一满级。未写精英阶段时前端按稀有度等级上限推断，结果仍需要正文确认。
4. v3 作业的模组编号：-1 默认、不切换；0 初始模组；1 X；2 Y；3 A；4 D。不要套用一图流另一个匹配器的枚举顺序。v2 作业把编号视为干员模组数组索引，原生前端先迁移再匹配；自行处理旧作业必须执行相同迁移或转网页复核。
5. 原生模组检查只要求指定类型等级至少 1；没有证明作者正文的二级／三级模组条件满足。源码也没有在此检查潜能、信赖、皮肤等条件。

原生分类规则（槽位数 N，缺失槽位数 M，练度不足槽位数 T）：

| 条件 | 分类 |
| --- | --- |
| N > 13 或 M >= 2 | `blocked` |
| M = 1 且 T = 0 | `borrow` |
| M = 1 且 T > 0 | `train` |
| M = 0 且 T = 0，N < 13 | `ready` |
| M = 0 且 T = 0，N = 13 | `borrow`（存在助战槽位需求） |
| M = 0 且 T = 1，N < 13 | `borrow`（可借达标的同名干员） |
| 其他练度不足情况 | `train` |

分类是初筛。原生组匹配分别计算每组，不做全局去重分配；同一干员可能被多个组重复选中。推荐前应检验有无互不冲突的实际阵容，并处理助战最多一人及自有编队容量。作者未填 `requirements` 时前端会视为满足，不代表最低练度真的无限制。

还需读取 `doc.details`：摆放顺序、手动操作、装置、核心模组、练度上下限、额外携带干员限制、作者宣布失效／新作业替代等可能只写在正文。返回 `available` 或高评分不能覆盖正文中的限制。

作业链接用 `https://prts.plus/?op=<id>`；当前分享代码为 `prts://<id>`，作业集为 `prts://s<id>`，两者不同。不能把纯数字代码随意当作视频或关卡编号。

## 已查证来源

- [PRTS Plus 官方前端及文档入口](https://github.com/ZOOT-Plus/zoot-plus-frontend)：README 说明暂无常驻后端接口文档，可查 TS 客户端类型或后端 Actions 的 OpenAPI artifact。
- [原生一图流导入组件](https://github.com/ZOOT-Plus/zoot-plus-frontend/blob/main/src/components/OperatorMatcher.tsx)
- [干员归一化与分类实现](https://github.com/ZOOT-Plus/zoot-plus-frontend/blob/main/src/models/operatorMatcher.ts)
- [查询参数与分页实现](https://github.com/ZOOT-Plus/zoot-plus-frontend/blob/main/src/apis/operation.ts)
- [旧作业模组迁移](https://github.com/ZOOT-Plus/zoot-plus-frontend/blob/main/src/models/converter.ts)
- [模组协议枚举](https://github.com/ZOOT-Plus/zoot-plus-frontend/blob/main/src/models/copilot.schema.ts)
- [关卡难度处理](https://github.com/ZOOT-Plus/zoot-plus-frontend/blob/main/src/models/level.ts)
- [分享代码实现](https://github.com/ZOOT-Plus/zoot-plus-frontend/blob/main/src/models/shortCode.ts)
- [官方后端源码](https://github.com/ZOOT-Plus/ZootPlusBackend)
- [一图流匹配器](https://ark.yituliu.cn/tools/operator-zoot-matcher)：本次读取的线上资源为 `/assets/operator-zoot-matcher-C6abJTsc.js`，构建哈希会改变。
- [PRTS Wiki](https://prts.wiki/)：主页确认其为资料 Wiki；本次匿名请求 MediaWiki `api.php?action=query...` 返回 403，未确认可供本环境使用的 Wiki API。不能据此断言该站没有 API。
