# 导入配置文件
import config
# 导入数据库检查
from module.utils import sql_funcs
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

# 数据库与Token检查
if not sql_funcs.sql_start_check():
    print("数据库错误")
    exit(1)
if config.Token == "":
    print("请先在config.py中输入对应Token后使用")
    exit(1)

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
