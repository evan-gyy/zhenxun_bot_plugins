import random
import os
import re
from pathlib import Path
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, PrivateMessageEvent, GroupMessageEvent, MessageSegment

dir_path = Path(__file__).parent
IMG_PATH = str((dir_path / "meme").absolute()) + "/"
RECORD_PATH = str((dir_path / "record").absolute()) + "/"

__zx_plugin_name__ = "随机莲莲"
__plugin_usage__ = """
usage：
    随机莲莲
    指令：
        莲莲/随机莲莲：发送莲莲表情包
        莲莲骂?[对象]：发送莲莲藏话
        爱国：发送莲莲爱国表情
        罕见：发送莲莲罕见语音
        
        示例：随机莲莲
        示例：莲莲骂我
""".strip()
__plugin_des__ = "随机莲莲"
__plugin_cmd__ = [
    "莲莲/随机莲莲/莲莲骂/爱国/罕见",
]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["莲莲", "随机莲莲", "莲莲骂", "爱国", "罕见"],
}
__plugin_block_limit__ = {"rst": "我知道你很急，但你先别急"}

dxl = on_command("莲莲", aliases={"随机莲莲", "莲莲表情包"}, priority=5, block=True)
dxl_zh = on_command("莲莲骂", priority=4, block=True)
dxl_hj = on_command("罕见", priority=5, block=True)
dxl_ag = on_command("爱国", priority=5, block=True)


@dxl.handle()
async def _(bot: Bot, event: Event):
    img = random_file(IMG_PATH, '\d+')
    image_file = f"file:///{IMG_PATH}/{img}"
    await dxl.finish(MessageSegment.image(image_file))

@dxl_zh.handle()
async def _(bot: Bot, event: Event):
    record = random_file(RECORD_PATH + '/zh')
    record_file = f"file:///{RECORD_PATH}/zh/{record}"
    await dxl.finish(MessageSegment.record(record_file))

@dxl_hj.handle()
async def _(bot: Bot, event: Event):
    record = random_file(RECORD_PATH + '/hj')
    record_file = f"file:///{RECORD_PATH}/hj/{record}"
    await dxl.finish(MessageSegment.record(record_file))

@dxl_ag.handle()
async def _(bot: Bot, event: Event):
    ag_img = random_file(IMG_PATH, 'ag\d+')
    image_file = f"file:///{IMG_PATH}/{ag_img}"
    await dxl.finish(MessageSegment.image(image_file))

def random_file(path, regex='\d+', end='\.\w+'):
    file_list = os.listdir(path)
    match_list = []
    for file in file_list:
        match = re.match(f'{regex}{end}', file)
        if match:
            match_list.append(file)
    return random.choice(match_list)