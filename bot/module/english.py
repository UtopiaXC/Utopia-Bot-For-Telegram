import datetime
import json
import random
import time

import requests
from bs4 import BeautifulSoup
from telegram.ext import (
    CommandHandler
)


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

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "英文原文：" + english
                     + "\n翻译：" + chinese
                     + "\n封面：")
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=pic
            )
            context.bot.send_voice(
                chat_id=update.effective_chat.id,
                voice=voice
            )
        except Exception as e:
            user = update.effective_user.name+"：\n"

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "服务器错误，错误原因：" + str(e)
            )

    handler = CommandHandler('english', english)
    dispatcher.add_handler(handler)
