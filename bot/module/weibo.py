import time

import requests
from bs4 import BeautifulSoup
from telegram.ext import (
    CommandHandler
)
from .utils.logger import info, warning, error

def add_weibo_plugin(dispatcher):
    # 微博
    def weibo(update, context):
        user = update.effective_user.name + "：\n"
        user_id = str(update.effective_user.id)
        user_name = str(update.effective_user.name)
        log_text = user_name + "(" + user_id + ")" + "由于微博热搜接口已失效，该功能已下线"
        error("微博热搜模块："+log_text)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=user + "由于微博热搜接口已失效，该功能已下线"
        )
    handler = CommandHandler('weibo', weibo)
    dispatcher.add_handler(handler)
