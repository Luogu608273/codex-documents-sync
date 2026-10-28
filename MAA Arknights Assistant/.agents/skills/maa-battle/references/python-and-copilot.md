# Python SDK 与自动战斗

## 依据与版本

核实日期：2026-10-10。本机核心实际加载为 v6.18.0，读取了安装目录 `Python/asst/asst.py`、`utils.py` 和 `sample.py`。线上文档可能描述更新功能，发生差异时以本机版本源码和实际返回为准。

- [官方 Python 封装，v6.18.0](https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/v6.18.0/src/Python/asst/asst.py)
- [官方 Python 示例，v6.18.0](https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/v6.18.0/src/Python/sample.py)
- [官方 CopilotTask 实现，v6.18.0](https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/v6.18.0/src/MaaCore/Task/Interface/CopilotTask.cpp)
- [集成文档](https://docs.maa.plus/zh-cn/protocol/integration.html)
- [战斗流程协议](https://docs.maa.plus/zh-cn/protocol/copilot-schema.html)
- [回调消息协议](https://docs.maa.plus/zh-cn/protocol/callback-schema.html)
- [自动战斗使用说明](https://docs.maa.plus/zh-cn/manual/introduction/copilot.html)

## 封装中实际存在的方法

| 方法 | 行为与返回 |
| --- | --- |
| `Asst.load(path, incremental_path=None, user_dir=None)` | 类静态方法，加载核心和资源，返回 bool；path 为安装根目录，非 resource 子目录 |
| `Asst(callback=None, arg=None)` | 创建独立实例；回调使用 `Asst.CallBackType` |
| `set_instance_option(option_type, option_value)` | 选项值为字符串，返回 bool |
| `connect(adb_path, address, config="General")` | 同步连接，返回 bool；config 为资源中已定义的连接配置 |
| `append_task(type_name, params)` | Python 字典参数，返回 task ID，0 表示失败 |
| `set_task_params(task_id, params)` | 返回 bool；部分字段不能运行中修改，Copilot 复制任务后不能再次设置 |
| `start()` / `running()` / `stop()` | bool；stop 同时清空本实例任务队列 |
| `get_version()` | 核心版本字符串 |
| `get_image(size)` | 上一次缓存截图，非主动刷新；当前封装返回整个分配缓冲区，不裁剪到实际 got 长度 |

本机 Python 封装没有公开 `async_screencap()`、`close()` 或上下文管理器。C 接口存在额外能力不代表 Python 有同名方法；不要凭 C 文档虚构 Python 调用。优先用 ADB 获取新 PNG，不把 `get_image()` 当作实时截图或确定格式的 BGR。

实例通过析构释放。持有实例和 ctypes callback 强引用直到任务结束，不手动重复调用析构；独立进程退出也是清理边界。设置选项可用本机 `asst.utils.InstanceOptionType`：

- `touch_type`（2）：例如 `"maatouch"`；根据实际连接能力选择，不为学习擅自更换 GUI 配置。
- `deployment_with_pause`（3）：`"1"` 开启暂停部署，影响抄作业；与作者要求核对。
- `kill_on_adb_exit`（5）：`"0"`，共享现有 ADB 服务时避免实例退出杀掉 ADB。

官方 `sample.py` 会先调用更新器，再启动包含作战、基建、购物的多个任务，且使用忙轮询；不要直接执行它来做只读连通性测试。

## Copilot 参数和准备

从 PRTS Plus 详情取出 `content` 后再 JSON 解码；MAA `filename` 指向这份作战 JSON，不是带 HTTP 包装的查询响应，也不是网页链接。保存原版并保留作业 ID、来源、修改内容。

任务常用参数（v6.18.0 CopilotTask 已核实）：

| 参数 | 用法 |
| --- | --- |
| `filename` | 单份 JSON 文件路径；使用绝对路径减少工作目录歧义 |
| `loop_times` | 单文件模式的次数，默认 1；指定有限正整数 |
| `use_sanity_potion` | 默认 false；true 在不足时允许使用理智药，接口不是药数量上限 |
| `formation` / `formation_index` | 是否自动编队 / 0 当前队伍，1–4 指定队伍；自动编队会改队伍 |
| `user_additional` | 自动编队追加的 `{name, skill}` 列表，技能 1–3；没有本次需要就省略 |
| `add_trust` | 默认 false；是否自动补信赖干员，作者禁止加人时关闭 |
| `ignore_requirements` | 默认 false；不以绕过练度要求制造“匹配成功” |
| `support_unit_usage` | 自动编队时：0 不借；1 缺一人时尝试借，否则不借；2 缺一人时借，否则借指定人；3 缺一人时借，否则随机借 |
| `support_unit_name` | 模式 2 的指定助战名；多于一人缺口不能靠单助战补齐 |
| `copilot_list` | 多作业数组，各项 filename、可选 nav_name_override、is_raid；与 filename 二选一。两者都有时 filename 优先 |

列表模式由核心导航，但需从关卡所在的地图页面开始，且列表处于同一区域、只需左右滑动即可找到；不能假定它从终端跨活动导航。单 `filename` 模式按官方说明先进入带“开始行动”按钮的编队选择界面。列表模式及单文件循环复制任务后不能再次 `set_task_params`。普通与突袭、磨难等难度必须先核对，不把 `stage_name` 相同当作难度已选对。

作战 JSON 的关键字段：`stage_name`、`opers`、`groups`、`actions`、`minimum_required`、作者 `doc`。最低版本、干员组替代、指定技能与模组、手动步骤都要读。战斗 `location` 是关卡格子坐标，不是 ADB 屏幕坐标。技能 `skill_usage` 与每条 action 各有含义，按协议和作者配置执行，不能随意换成“好了就放”。

## 有界执行示例

以下是供后续用户要求作战时采用的调用片段，需传入已核对的文件、连接配置与编队；本次学习没有运行此片段。`formation=False` 表示当前队伍已手动准备好。若任务要求自动编队，再按本次选择改为 true 并指定栏位和助战。

```python
import json
import queue
import sys
import time
from pathlib import Path

maa_dir = Path(r"D:\MAA-Arknights-Assistant")
sys.path.insert(0, str(maa_dir / "Python"))
from asst.asst import Asst
from asst.utils import InstanceOptionType

events = queue.SimpleQueue()

@Asst.CallBackType
def callback(message, details, arg):
    # 原生线程回调：保留未知消息编号，不在回调内阻塞或重入复杂接口。
    try:
        events.put((message, json.loads(details.decode("utf-8")) if details else {}))
    except Exception as exc:
        events.put((message, {"decode_error": str(exc)}))

def run_one(copilot_file, adb_path, serial, config, user_dir, timeout_seconds):
    if timeout_seconds <= 0:
        raise ValueError("A positive run deadline is required")
    copilot_file = Path(copilot_file).resolve(strict=True)
    user_dir = Path(user_dir).resolve()
    user_dir.mkdir(parents=True, exist_ok=True)
    if not Asst.load(maa_dir, user_dir=user_dir):
        raise RuntimeError("Resource loading failed")
    asst = Asst(callback)
    if not asst.set_instance_option(InstanceOptionType.kill_on_adb_exit, "0"):
        raise RuntimeError("Instance option rejected")
    if not asst.connect(str(adb_path), serial, config):
        raise RuntimeError("Connect failed")
    task_id = asst.append_task("Copilot", {
        "filename": str(copilot_file), "loop_times": 1,
        "formation": False, "use_sanity_potion": False,
        "add_trust": False, "ignore_requirements": False,
        "support_unit_usage": 0,
    })
    if task_id == 0:
        raise RuntimeError("Task rejected; inspect file/version/stage/resources")
    if not asst.start():
        raise RuntimeError("Start failed")
    deadline = time.monotonic() + timeout_seconds
    try:
        with (user_dir / "events.jsonl").open("a", encoding="utf-8") as log:
            while True:
                while not events.empty():
                    message, details = events.get()
                    log.write(json.dumps({"message": message, "details": details}, ensure_ascii=False) + "\n")
                    log.flush()
                if not asst.running():
                    break
                if time.monotonic() >= deadline:
                    raise TimeoutError("Run deadline reached; inspect before retrying")
                time.sleep(1)  # 状态轮询，无截图。
    finally:
        asst.stop()  # 此实例任务清空；结果仍须结合回调及结算复核。
```

示例没有自动更新、唤醒、导航、改编队和判胜逻辑。结合所选模式补足准备和最终结算观察后再执行；不要把片段返回当作通关证据。

## Fight 代理刷关

关卡使用游戏编号，例如 `"1-7"`，不要照搬作业站检索 ID `main_01-07`。任务参数的有界基线：

```python
params = {
    "stage": "1-7", "times": 1, "series": 1,
    "medicine": 0, "medicine_expire_days": 0, "stone": 0,
    "report_to_penguin": False, "report_to_yituliu": False,
}
# 仅在本次授权的是代理刷关时 append_task("Fight", params)。
```

默认 `times=2147483647`；明确次数和代理倍率，避免把“一次测试”变成持续刷关。药品与源石开关必须符合本次消耗范围。`Fight` 不能替代尚无代理的首次 Copilot 通关。

## 回调、故障与结果

本机 `utils.Message`：`3 AllTasksCompleted`；`10000 TaskChainError`、`10001 Start`、`10002 Completed`、`10004 Stopped`；`20000 SubTaskError`、`20002 SubTaskCompleted`、`20003 SubTaskExtraInfo`。详细事件有 taskchain、what、details，保留完整结构。单个子任务错误可能涉及重试，不能脱离后续事件就宣称整场失败；链错误、断连或不支持分辨率时停止推进并诊断。

重点差异：v6.18.0 `CopilotTask.cpp` 的单文件路径设置 `set_wait_until_end(false)`，列表路径设置 true 并安排结算检查。因此单文件的任务完成尤其不能证明已经战斗结算。先读 callbacks / `user_dir/debug/asst.log`，关键节点低频取图；观察结算星级、失败提示与目标难度后报告结果。没有结算证据就如实说执行已结束、结果待复核。

ADB 设备 `device` 只代表传输通畅；connect 成功只代表识别连接成功。连接或运行失败时不擅自换设备、关卡或触控方式重试，不通过重启共享 ADB 服务干扰正在运行的 GUI。
