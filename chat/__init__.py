import asyncio
from nonebot import on_command, on_message, require
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from nonebot.log import logger
import openai
import requests
from openai.error import APIError, APIConnectionError, RateLimitError, AuthenticationError

api_key = ""     # 修改你的api_key
openai.api_key = api_key

__zx_plugin_name__ = "chat"
__plugin_usage__ = """
usage：
    ChatGPT
    指令：
        chat [问题]：与ChatGPT对话
        重置chat：重置对话历史（默认保留10轮对话）
        查询chat：查询余额
""".strip()
__plugin_des__ = "ChatGPT"
__plugin_cmd__ = ["chat"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "evan-gyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__,
}
__plugin_cd_limit__ = {
    "cd": 10,
    "rst": "CD中，别急"
}

chat = on_command("chat", priority=5, block=True)
reset = on_command("重置chat", priority=5, block=True)
query = on_command("查询chat", priority=5, block=True)

history = {}
max_ctx = 10


@chat.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    global history
    msg = arg.extract_plain_text().strip()
    if not msg:
        return await chat.send(__plugin_usage__)

    chat_id = str(event.group_id) if isinstance(event, GroupMessageEvent) else str(event.user_id)
    conv = history.get(chat_id, [])

    try:
        if not conv:
            history[chat_id] = conv
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, ask, msg, conv)
    except APIError as e:
        # API error
        logger.error(f"OpenAI API returned an API Error: {e}")
        return await chat.finish("API错误，请稍后重试")
    except APIConnectionError as e:
        # Handle connection error here
        logger.error(f"Failed to connect to OpenAI API: {e}")
        return await chat.finish("网络连接异常")
    except RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        logger.error(f"OpenAI API request exceeded rate limit: {e}")
        return await chat.finish("请求数达上限")
    except Exception as e:
        logger.error(str(e))
        return await chat.finish("未知错误，请联系管理员")

    conv.append({"role": "user", "content": msg})
    conv.append({"role": "assistant", "content": response})

    conv = conv[2:] if len(conv) > max_ctx * 2 else conv
    history[chat_id] = conv

    await chat.send(response, at_sender=True)


@reset.handle()
async def _(event: MessageEvent):
    global history
    try:
        if isinstance(event, GroupMessageEvent):
            history.pop(str(event.group_id))
        else:
            history.pop(str(event.user_id))
    except Exception as e:
        logger.error(str(e))
    await reset.send("chat已重置")


@query.handle()
async def _(event: MessageEvent):
    try:
        loop = asyncio.get_event_loop()
        total, available, delta = await loop.run_in_executor(None, get_credit_available)
    except Exception as e:
        logger.error(str(e))
        return await query.finish("查询失败，请重试")

    msg = f"\n额度总量：$ {total}\n已用额度：$ {delta}\n剩余额度：$ {available}"
    await query.send(msg, at_sender=True)


def ask(msg, conv):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conv + [{"role": "user", "content": msg}]
    )
    logger.info(completion)
    return '\n' + completion.choices[0].message.content.strip()


def get_credit_available():
    url = "https://api.openai.com/dashboard/billing/credit_grants"
    headers = {"Authorization": f"Bearer {api_key}"}
    res = requests.get(url=url, headers=headers)
    credit = res.json()
    total = credit['total_granted']
    available = credit['total_available']
    delta = round(total - available, 6)
    return total, available, delta