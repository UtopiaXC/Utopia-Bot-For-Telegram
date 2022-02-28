from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from . import logger

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57 "
}


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.effective_user.name + "：\n"
    user_id = str(update.effective_user.id)
    user_name = str(update.effective_user.name)
    log_text = user_name + "(" + user_id + ")" + "取消了当前正在运行的命令"
    logger.warning(log_text)
    update.message.reply_text(
        user + '命令结束'
    )
    return ConversationHandler.END
