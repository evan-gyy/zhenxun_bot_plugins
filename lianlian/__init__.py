import random
import json
import os
import re
import gensim
import jieba
from queue import PriorityQueue as PQ
from pathlib import Path
from nonebot import on_command, on_keyword
from nonebot.typing import T_State
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message

dir_path = Path(__file__).parent
IMG_PATH = str((dir_path / "meme").absolute()) + "/"
RECORD_PATH = str((dir_path / "record").absolute()) + "/"
DATA_PATH = str((dir_path / "data").absolute()) + "/"

__zx_plugin_name__ = "随机莲莲"
__plugin_usage__ = """
usage：
    随机莲莲
    指令：
        莲莲/随机莲莲：发送莲莲表情包
        莲莲骂?[对象]：发送莲莲藏话
        狗叫 ?[长/短]：发送莲莲狗叫
        爱国：发送莲莲爱国表情
        罕见：发送莲莲罕见语音
        
        示例：随机莲莲
        示例：莲莲骂我
        示例：狗叫 长
""".strip()
__plugin_des__ = "随机莲莲"
__plugin_cmd__ = ["莲莲/随机莲莲/莲莲骂/爱国/罕见/狗叫"]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__,
}
__plugin_block_limit__ = {"rst": "我知道你很急，但你先别急"}


dxl = on_keyword({"莲莲", "随机莲莲", "罕见", "爱国"}, priority=5, block=True)
dxl_gj = on_command("狗叫", priority=5, block=True)
dxl_zh = on_command("莲莲骂", priority=4, block=True)


@dxl.handle()
async def _(bot: Bot, event: Event):
    text = event.get_plaintext().strip()
    if "罕见" in text:
        file = random_file(RECORD_PATH + '/hj')
        await dxl.finish(MessageSegment.record(file))
    elif "爱国" in text:
        file = random_file(IMG_PATH, 'ag\d+')
        await dxl.finish(MessageSegment.image(file))
    elif "莲莲" in text:
        if text == "莲莲":
            file = random_file()
        else:
            logger.info("开始寻找相似表情包...")
            file = similar_meme(text.replace("莲莲", "").strip(), 3)
        await dxl.finish(MessageSegment.image(file))


@dxl_gj.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    text = args.extract_plain_text().strip().split()
    path = RECORD_PATH + '/gj'
    file = random_file(path, '.*')
    if text:
        if "长" in text:
            file = random_file(path, 'long\d+')
        elif "短" in text:
            file = random_file(path, '\d+')
    await dxl_gj.finish(MessageSegment.record(file))


@dxl_zh.handle()
async def _(bot: Bot, event: Event):
    record = random_file(RECORD_PATH + '/zh')
    await dxl_zh.finish(MessageSegment.record(record))


def similar_meme(sentence, n=3):
    vector_path = DATA_PATH + 'sgns.weibo.bigram-char.bin'
    wv = gensim.models.KeyedVectors.load(vector_path, mmap='r')
    with open(DATA_PATH + 'meme.json', 'r', encoding='utf-8') as f:
        meme = json.load(f)
    cut = jieba.lcut(sentence)
    sims = PQ()
    for k, v in meme.items():
        sm = wv.n_similarity(cut, jieba.lcut(v))
        sims.put([1-sm, k])
    res = []
    for _ in range(n):
        res.append(sims.get()[-1])
    if random.random() <= 0.8:
        return f"file:///{IMG_PATH}/" + res[0] + '.jpg'
    else:
        return f"file:///{IMG_PATH}/" + random.choice(res) + '.jpg'


def random_file(path=IMG_PATH, regex='\d+', end='\.\w+'):
    file_list = os.listdir(path)
    match_list = []
    for file in file_list:
        match = re.match(f'{regex}{end}', file)
        if match:
            match_list.append(file)
    return f"file:///{path}/{random.choice(match_list)}"