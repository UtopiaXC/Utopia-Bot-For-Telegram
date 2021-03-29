import time

import requests
from bs4 import BeautifulSoup
from telegram.ext import (
    CommandHandler
)
from module.utils.logger import info, warning, error

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
            user = update.effective_user.name+"：\n"
            info("微博热搜模块："+user+"获取了当前热搜")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + res)
        except Exception as e:
            user = update.effective_user.name+"：\n"
            error("微博热搜模块：服务器获取热搜异常或发送消息异常")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "服务器错误，错误原因：" + str(e)
            )

    handler = CommandHandler('weibo', weibo)
    dispatcher.add_handler(handler)
