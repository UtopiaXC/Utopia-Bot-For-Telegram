import datetime
import json
import random
import time

import requests
from telegram.ext import (
    CommandHandler
)
from .utils.logger import info, warning, error

def add_english_plugin(dispatcher):
    # 每日英语
    def english(update, context):
        try:
            end_time = datetime.datetime.now()
            start_time = datetime.datetime.now() + datetime.timedelta(days=-600)
            a1 = tuple(start_time.timetuple()[0:9])
            a2 = tuple(end_time.timetuple()[0:9])
            start = time.mktime(a1)
            end = time.mktime(a2)
            t = random.randint(int(start), int(end))
            date_touple = time.localtime(t)
            date = time.strftime("%Y-%m-%d", date_touple)
            res = requests.get("http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=" + date)
            json_str = json.loads(res.text)
            chinese = json_str["note"]
            english = json_str["content"]
            pic = json_str["picture2"]
            voice = json_str["tts"]
            user = update.effective_user.name+"：\n"
            text=user + "英文原文：" + english\
                     + "\n翻译：" + chinese\
                     + "\n封面："
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" + "获取了一条每日英语：" + english
            info("每日英语模块："+log_text)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text)
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" + "发送图片：" + pic
            info("每日英语模块：" + log_text)
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=pic
            )
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" + "发送音频：" + voice
            info("每日英语模块：" + log_text)
            context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=voice
            )
        except Exception as e:
            user = update.effective_user.name+"：\n"
            text=user + "服务器错误，错误原因：" + str(repr(e))
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" +"服务器错误，错误原因：" + str(repr(e))
            error("每日英语模块："+log_text)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )

    handler = CommandHandler('english', english)
    dispatcher.add_handler(handler)
