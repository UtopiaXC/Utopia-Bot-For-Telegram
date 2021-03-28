from telegram import Update
from telegram.ext import (
    CommandHandler
)


def add_start_plugin(dispatcher):
    # 开始功能
    def start(update: Update, context):
        user = update.effective_user.username
        user = "@" + user + "：\n"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=user + "欢迎使用Utopia机器人，请使用 /help 查看全部指令"
        )

    handler = CommandHandler('start', start)
    dispatcher.add_handler(handler)
