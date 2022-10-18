from typing import Tuple, Any
from nonebot import on_regex
from nonebot.params import RegexGroup
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

__zx_plugin_name__ = "色图盲盒"
__plugin_usage__ = """
usage：
    色图盲盒
    指令：
        ?[N连]盲盒
        示例：盲盒
        示例：3连盲盒 （单次请求张数小于等于5）
""".strip()
__plugin_des__ = "色图盲盒"
__plugin_cmd__ = ["盲盒"]
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__,
}

blind_box = on_regex(r"^(\d?)连?(盲盒)$", priority=5, block=True)

# 色图盲盒API, 0.05%概率出涩图
url = "https://iw233.cn/API/Random.php"


@blind_box.handle()
async def _(bot: Bot, event: MessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    num = reg_group[0] or 1
    for _ in range(min(int(num), 5)):
        try:
            await blind_box.send(MessageSegment.image(url))
        except Exception as e:
            await blind_box.send("你开给我看！")
            logger.error(f"blind_box 发送了未知错误 {type(e)}：{e}")
