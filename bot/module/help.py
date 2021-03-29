from telegram.ext import (
    CommandHandler
)


def add_help_plugin(dispatcher):
    # 指令帮助
    def help(update, context):
        user = update.effective_user.name+"：\n"

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=user + "/start - 开始\n"
                        "/help - 获得全部指令帮助\n"
                        "/cancel - 终止当前进行中的任务（当机器人不响应的时候请选择）\n"
                        "/stock - 股票信息查询\n"
                        "/stock_mine - 快速查询自选股\n"
                        "/setu - 获取一张随机涩图\n"
                        "/sentence - 一言：获取随机一句名句\n"
                        "/weibo - 获取微博热搜\n"
                        "/zhihu - 随机获取一条知乎日报\n"
                        "/bili - 随机获取一条bilibili热榜视频\n"
                        "/english - 随机获取一条每日英语"
        )

    handler = CommandHandler('help', help)
    dispatcher.add_handler(handler)
