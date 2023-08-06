import re

from EdgeGPT import Chatbot
from pydantic import BaseModel

from nonebot import get_driver
from nonebot.log import logger

from ..config import Config
from ..exceptions import BaseBingChatException, BingChatResponseException


plugin_config = Config.parse_obj(get_driver().config).dict()


class BingChatResponse(BaseModel):
    raw: dict

    @property
    def content_simple(self) -> str:
        try:
            return removeQuoteStr(self.raw["item"]["messages"][1]["text"])
        except (IndexError, KeyError) as exc:
            logger.error(self.raw)
            raise BingChatResponseException('无法解析响应值内容') from exc


class Conversation(BaseModel):
    ask: str
    reply: BingChatResponse


def helpMessage() -> str:
    return (
        f"""命令符号：{''.join(f'"{i}"' for i in plugin_config['command_start'])}\n"""
        f"""开始对话：{{命令符号}}{'/'.join(i for i in plugin_config['bingchat_command_chat'])} + {{你要询问的内容}}\n"""
        f"""重置一个对话：{{命令符号}}{'/'.join(i for i in plugin_config['bingchat_command_new_chat'])}"""
    )


def removeQuoteStr(string: str) -> str:
    return re.sub(r'\[\^\d\^\]', '', string)
