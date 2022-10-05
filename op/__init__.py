import random
import json
import os
from pathlib import Path
from nonebot import on_command, on_keyword
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, GroupMessageEvent, PrivateMessageEvent

dir_path = Path(__file__).parent
POST_PATH = str((dir_path / "resource").absolute()) + "/"

__zx_plugin_name__ = "OP语录"
__plugin_usage__ = """
usage：
    OP语录
    指令：
        op/op语录/来点op/原神 ?[关键词]：随机op语录，输入关键词可以匹配相关语录
        示例：op 差不多得了
""".strip()
__plugin_des__ = "OP语录"
__plugin_cmd__ = ["op", "op语录", "来点op", "原神"]
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

op_posts = on_command("op", aliases={"op语录", "来点op", "原神"}, priority=5, block=True)

@op_posts.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip().split()
    with open(POST_PATH + "posts.json", 'r', encoding='utf-8') as f:
        posts = json.load(f)['op']
    res = random.choice(posts)
    logger.info(res)
    if msg:
        matches = [i for i in posts if msg[0] in i]
        if matches:
            res = random.choice(matches)
    messages = [{
        "type": "node",
        "data": {
            "name": "真寻",
            "uin": f"{bot.self_id}",
            "content": [
                {"type": "text", "data": {"text": res}},
            ],
        },
    }]
    if len(res) > 250 and isinstance(event, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)
    else:
        await op_posts.finish(res)
