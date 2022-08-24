import random
from datetime import date
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message

__zx_plugin_name__ = "今日人品"
__plugin_usage__ = """
usage：
    获取今日人品值
    指令：
        jrrp/今日人品
""".strip()
__plugin_des__ = "今日人品"
__plugin_cmd__ = ["jrrp/今日人品"]
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["jrrp", "今日人品"],
}

jrrp = on_keyword({'jrrp', '今日人品'}, priority=5, block=True)

@jrrp.handle()
async def _(bot: Bot, event: Event):
    id = event.get_user_id()
    seed = int(date.today().strftime("%y%m%d")) + int(id)
    random.seed(seed)
    luck = random.randint(1, 100)
    session = event.get_session_id()
    if session.startswith("group"):
        msg = f"[CQ:at,qq={id}]今天的人品值是：{luck}"
    else:
        msg = f"您今天的人品值是：{luck}"
    await jrrp.finish(Message(msg))