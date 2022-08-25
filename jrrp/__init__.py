import random
import os
import re
import json
import time
from datetime import date, datetime
from nonebot.plugin import on_keyword, on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent
from nonebot.adapters.onebot.v11.message import Message

dir = os.path.dirname(__file__)
DATA_PATH = {
    "tarot": dir + "/data/TarotData.json"
}

__zx_plugin_name__ = "今日人品"
__plugin_usage__ = """
usage：
    今日人品等骰娘指令复刻
    指令：
        .jrrp/今日人品: 获取今日人品值
        .draw ?[数量]张塔罗牌: 抽取塔罗牌，上限为5张
        .rc [技能] ?[概率]: 技能鉴定，默认概率为今日人品值
        
        示例: .draw 3张塔罗牌
        示例: .rc 睡觉 80
""".strip()
__plugin_des__ = "今日人品等骰娘指令复刻"
__plugin_cmd__ = [".jrrp/今日人品/.draw/.rc"]
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__,
}

jrrp = on_command(".jrrp", aliases={'今日人品'}, priority=5, block=True)
draw = on_command(".draw", priority=5, block=True)
rc = on_command(".rc", priority=5, block=True)

@jrrp.handle()
async def _(event: Event):
    id = event.get_user_id()
    luck = get_luck(id)
    session = event.get_session_id()
    if session.startswith("group"):
        msg = f"[CQ:at,qq={id}]今天的人品值是：{luck}"
    else:
        msg = f"您今天的人品值是：{luck}"
    await jrrp.finish(Message(msg))


@draw.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    n = 1
    if msg:
        if match := re.match("(\d+)张塔罗牌", msg[0]):
            n = int(match.group(1))
    user_name = event.sender.card or event.sender.nickname
    if n == 1:
        await draw.finish(f"来看看{user_name}抽到了什么:\n" + draw_card("tarot"))
    elif 1 < n <= 5:
        for i in range(n):
            await draw.send(f"{user_name}抽到的第{i+1}张牌是:\n" + draw_card("tarot"))
            time.sleep(1)
    else:
        await draw.finish("抽牌数量必须在1-5之间！")


@rc.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    if msg:
        if (n := len(msg)) <= 2:
            seed = int(datetime.now().strftime('%y%m%d%H%M%S')) + int(hash(msg[0]))
            random.seed(seed)
            roll = random.randint(1, 100)
            luck = get_luck(event.get_user_id())
            if n == 2:
                try:
                    luck = int(msg[1])
                    print(luck)
                except:
                    await rc.finish("检定数值必须为整数！")
                else:
                    if luck < 1 or luck > 100:
                        await rc.finish("检定数值必须为[1-100]间的整数！")
            result = roll_success_level(roll, luck)
            user_name = event.sender.card or event.sender.nickname
            await rc.finish(f"{user_name}进行{msg[0]}检定: D100={roll}/{luck} {result}")
        else:
            await rc.finish("参数过多！")
    else:
        await rc.finish("请输入要检定的技能！")


def get_luck(id):
    seed = int(date.today().strftime("%y%m%d")) + int(id)
    random.seed(seed)
    luck = random.randint(1, 100)
    return luck


def roll_success_level(roll, luck):
    if roll == 100 and luck >= 50 or roll >= 96 and luck < 50:
        return "大失败"
    if roll == 1 and luck <= 50 or roll <= 5 and luck > 50:
        return "大成功"
    if roll <= luck / 5:
        return "极难成功"
    if roll <= luck / 2:
        return "困难成功"
    if roll <= luck:
        return "成功"
    else:
        return "失败"


def draw_card(deck="tarot"):
    path = DATA_PATH[deck]
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)[deck]
    card = random.choice(data)
    pos = random.choice(['positive', 'negative'])
    pos_zh = "正位" if pos == 'positive' else "逆位"
    desc = "【" + to_roman(data.index(card)+1) + "】" + card['name'] + f' {pos_zh}:\n' + card[pos]
    return desc


def to_roman(num: int) -> str:
    int_to_roman = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
                    (100,"C"),(90,"XC"),(50,"L"),(40,"XL"),
                    (10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
    roman_num = ""
    for number,roman in int_to_roman:
        count,num = divmod(num,number)
        roman_num += roman * count
        if num == 0:
            break
    return roman_num