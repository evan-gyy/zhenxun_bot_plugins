from random import shuffle, randint
import random
import os
from pathlib import Path
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, PrivateMessageEvent, GroupMessageEvent, MessageSegment

dir_path = Path(__file__).parent
IMG_PATH = str((dir_path / "meme").absolute()) + "/"

__zx_plugin_name__ = "随机莲莲"
__plugin_usage__ = """
usage：
    随机莲莲
    指令：
        莲莲/随机莲莲/莲莲表情包
""".strip()
__plugin_des__ = "随机莲莲表情包"
__plugin_cmd__ = [
    "莲莲/随机莲莲/莲莲表情包",
]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["莲莲", "随机莲莲", "莲莲表情包"],
}
__plugin_block_limit__ = {"rst": "我知道你很急，但你先别急"}

dxl = on_command("莲莲", aliases={"随机莲莲", "莲莲表情包"}, priority=5, block=True)


@dxl.handle()
async def _(bot: Bot, event: Event):
    index = random.randint(1, 25)
    image_file = f"file:///{IMG_PATH}/{index}.jpg"
    await dxl.finish(MessageSegment.image(image_file))
