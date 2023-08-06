from enum import Enum
from typing import Optional
from pydantic import BaseModel, Extra, validator


class filterMode(str, Enum):
    whitelist = 'whitelist'
    blacklist = 'blacklist'


class Config(BaseModel, extra=Extra.ignore):
    superusers: list[int] = []
    command_start: str | list[str] = []

    bingchat_command_chat: str | list[str] = ['chat']
    bingchat_command_new_chat: str | list[str] = ['chat-new', '刷新对话']
    bingchat_command_history_chat: str | list[str] = ['chat-history']

    bingchat_command_limit_rate: Optional[int] = None
    bingchat_command_limit_count: Optional[int] = None

    bingchat_group_filter_mode: filterMode = filterMode.blacklist
    bingchat_group_filter_blacklist: list[int] = []
    bingchat_group_filter_whitelist: list[int] = []

    @validator('bingchat_command_chat')
    def bingchat_command_chat_validator(cls, v):
        return list(v)

    @validator('bingchat_command_new_chat')
    def bingchat_command_new_chat_validator(cls, v):
        return list(v)
