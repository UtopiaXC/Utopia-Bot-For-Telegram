# 导入配置文件
import sys

import config
# 导入初始化检查
from module.utils import sql_funcs
from module.utils.logger import logger_start_check
from module.utils.logger import info, warning, error
# 加载telegram-bot
from telegram.ext import Updater

# 加载模块
import module.stocks as stocks
import module.start as start
import module.help as help
import module.setu as setu
import module.sentence as sentence
import module.bili as bili
import module.weibo as weibo
import module.english as english

logger_start_check()
info("主进程：日志文件检查完成")
info("主进程：开始进行数据库检查")
# 数据库与Token检查
if not sql_funcs.sql_start_check():
    error("主进程：数据库创建或读取错误，请检查")
    warning("主进程：程序由于异常导致退出")
    exit(1)
info("主进程：数据库检查完成")

if config.Token == "":
    error("主进程：配置文件错误，请先在config.py中输入对应Token后使用")
    warning("主进程：程序由于异常导致退出")
    exit(1)
info("主进程：配置文件检查完成")

# 初始化Telegram-Bot
updater = Updater(token=config.Token, use_context=True)
dispatcher = updater.dispatcher

# 将模块添加
stocks.add_stock_plugin(dispatcher)
start.add_start_plugin(dispatcher)
help.add_help_plugin(dispatcher)
setu.add_setu_plugin(dispatcher)
sentence.add_sentence_plugin(dispatcher)
bili.add_bili_plugin(dispatcher)
weibo.add_weibo_plugin(dispatcher)
english.add_english_plugin(dispatcher)

# 启动消息监听
updater.start_polling()
