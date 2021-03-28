import json
import random
import time

import requests
from telegram.ext import (
    CommandHandler
)


def add_zhihu_plugin(dispatcher):
    # 知乎日报
    def zhihu(update, context):
        try:
            res = requests.get("https://news-at.zhihu.com/api/3/stories/latest", headers=header)
            json_str = json.loads(res.text)
            index = random.randint(0, len(json_str["stories"]) - 1)
            title = json_str["stories"][index]["title"]
            url = json_str["stories"][index]["url"]
            localtime = time.asctime(time.localtime(time.time()))
            user = update.effective_user.username
            user = "@" + user + "：\n"
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + '北京时间:' + localtime + " 知乎日报"
                     + "\n文章标题：" + title
                     + "\n文章链接：" + url)
        except Exception as e:
            user = update.effective_user.username
            user = "@" + user + "：\n"
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "服务器错误，错误原因：" + str(e)
            )

    handler = CommandHandler('zhihu', zhihu)
    dispatcher.add_handler(handler)
