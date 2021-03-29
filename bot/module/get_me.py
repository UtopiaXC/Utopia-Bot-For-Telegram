from telegram.ext import (
    CommandHandler
)
from module.utils.logger import info, warning, error


def add_get_me_plugin(dispatcher):
    # 获取自身ID
    def get_me(update, context):
        try:
            user_id = update.effective_user.id
            user_name = update.effective_user.name
            info("用户名为" + user_name + "的用户获取了他的ID：" + str(user_id))
            text = user_name + "：\n" + "您的ID为" + str(user_id)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )
        except Exception as e:
            error("获取ID模块异常："+str(e))

    handler = CommandHandler('get_me', get_me)
    dispatcher.add_handler(handler)
