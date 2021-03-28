import time

import requests
from bs4 import BeautifulSoup
from telegram.ext import (
    CommandHandler
)


def add_weibo_plugin(dispatcher):
    # 微博
    def weibo(update, context):
        try:
            res = requests.get("https://s.weibo.com/top/summary")
            soup = BeautifulSoup(res.text)
            res = ""
            for i in range(len(soup.find_all("td", class_="td-02"))):
                if i == 0:
                    res += ("置顶热搜：" + soup.find_all("td", class_="td-02")[i].a.get_text() + '\n')
                else:
                    res += ("热搜第" + str(i) + "：" + soup.find_all("td", class_="td-02")[i].a.get_text() + '\n')
            localtime = time.asctime(time.localtime(time.time()))
            res += ('北京时间:' + localtime)
            user = update.effective_user.username
            user = "@" + user + "：\n"
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + res)
        except Exception as e:
            user = update.effective_user.username
            user = "@" + user + "：\n"
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "服务器错误，错误原因：" + str(e)
            )

    handler = CommandHandler('weibo', weibo)
    dispatcher.add_handler(handler)
