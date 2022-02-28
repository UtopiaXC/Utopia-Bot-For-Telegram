from telegram.ext import (
    CommandHandler
)
from .utils.logger import info, warning, error


def add_get_me_plugin(dispatcher):
    # 获取自身ID
    def get_me(update, context):
        try:
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" + "获取了他的ID"
            info("获取用户ID模块：" + log_text)
            text = user_name + "：\n" + "您的ID为" + str(user_id)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )
        except Exception as e:
            error("获取用户ID模块：异常："+str(e))

    handler = CommandHandler('get_me', get_me)
    dispatcher.add_handler(handler)
