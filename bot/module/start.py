from telegram import Update
from telegram.ext import (
    CommandHandler
)
from .utils.logger import info, warning, error


def add_start_plugin(dispatcher):
    # 开始功能
    def start(update: Update, context):
        try:
            user = update.effective_user.name + "：\n"
            info("用户：" + update.effective_user.name + "开始了与机器人的交流")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "欢迎使用Utopia机器人，请使用 /help 查看全部指令"
            )
        except:
            error("无法发送开始信息，请检查网络")

    handler = CommandHandler('start', start)
    dispatcher.add_handler(handler)
