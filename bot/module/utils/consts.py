from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from module.utils.logger import info, warning, error

SETU, SENTENCE, STOCK_FUNC, STOCK_MINE, STOCK_ADD_MINE, STOCK_DO_ADD_MINE, STOCK_DELETE_MINE, STOCK_SEARCH, STOCK_SELECT = range(
    9)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57 "
}


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.effective_user.name + "：\n"
    warning(update.effective_user.name + "取消了当前正在运行的命令")
    update.message.reply_text(
        user + '命令结束'
    )
    return ConversationHandler.END
