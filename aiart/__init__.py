import json
import wenxin_api
from wenxin_api.tasks.text_to_image import TextToImage
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.params import CommandArg, ArgStr

__zx_plugin_name__ = "AI绘画"
__plugin_usage__ = """
usage：
    生成AI画作
    指令：
        ai画 ?[风格] [prompt]：生成指定风格和内容的画作
        风格可选：
            卡通（默认）、古风、油画、水彩画、二次元、浮世绘、蒸汽波艺术、
            low poly、像素风格、概念艺术、未来主义、赛博朋克、写实风格、
            洛丽塔风格、巴洛克风格、超现实主义
        示例：
            ai画 卡通 少女，赛博朋克，未来感，高清，3d，cg感，
            精致面容，cg感，唯美，毛发细致，蓝色头发，上半身立绘
""".strip()
__plugin_des__ = "AI绘画"
__plugin_cmd__ = ["ai画"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["ai画"],
}

# 通过 https://wenxin.baidu.com/moduleApi/key 获取
API_KEY = ""
SECRET_KEY = ""

ai_art = on_command("ai画", block=True, priority=5)


@ai_art.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        matcher.set_arg("text", arg)


@ai_art.got("text", prompt="来点prompt")
async def _(bot: Bot, event: MessageEvent, text: str = ArgStr("text")):
    logger.info("prompt: " + text)
    if len(text) < 10:
        await ai_art.reject("prompt太短，重来（字数>10）")
    args = text.strip().split()
    style = args[0] if len(args) > 1 else "卡通"
    prompt_text = "".join(args[1:]) if len(args) > 1 else text
    await ai_art.send("少女绘画中...（预计1-3分钟）")
    try:
        rst = await get_ai_image(API_KEY, SECRET_KEY, prompt_text, style)
        if rst["imgUrls"]:
            image_list = rst["imgUrls"]
            logger.info(f"AI绘画生成结果：{image_list}")
            msg_list = [MessageSegment.image(img) for img in image_list]
            if isinstance(event, GroupMessageEvent):
                id = event.get_user_id()
                await ai_art.send(Message(f"[CQ:at,qq={id}]画完了！"))
                await bot.send_group_forward_msg(
                    group_id=event.group_id, messages=forward_image(bot, msg_list)
                )
            else:
                for m in msg_list:
                    await ai_art.send(m)
        else:
            await ai_art.send("你画给我看！")
            logger.error(f"绘画时发生错误：{rst}")
    except Exception as e:
        if type(e) == wenxin_api.error.APIError:
            ret = json.loads(e.args[0])
            await ai_art.send(ret["msg"])
        else:
            await ai_art.send("你画给我看！")
        logger.error(f"发生错误 {type(e).__name__}: {e}")


async def get_ai_image(api_key, secret_key, text, style="卡通"):
    wenxin_api.ak = api_key
    wenxin_api.sk = secret_key
    input_dict = {
        "text": text,
        "style": style
    }
    rst = TextToImage.create(**input_dict)
    return rst


def forward_image(bot, image_list):
    msg = []
    for img in image_list:
        data = {
            "type": "node",
            "data": {
                "name": "真寻",
                "uin": f"{bot.self_id}",
                "content": img,
            },
        }
        msg.append(data)
    return msg
