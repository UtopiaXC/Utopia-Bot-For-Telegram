import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)
import requests
import config
from module.utils.consts import (
    SETU,
    cancel
)


def add_setu_plugin(dispatcher):
    # 涩图功能-R18选择器
    def setu_input(update: Update, _: CallbackContext):
        keyboard = [
            [
                InlineKeyboardButton("R18", callback_data='R18'),
                InlineKeyboardButton("非R18", callback_data='非R18'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        user = update.effective_user.name+"：\n"

        update.message.reply_text(
            user + '请选择您需要的是R18还是非R18涩图',
            reply_markup=reply_markup,
        )
        return SETU

    # 涩图功能-涩图发送
    def setu(update: Update, _: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        query.delete_message()
        url = ""
        r18 = 0
        if query.data == "R18":
            r18 = 1
        try:
            res = requests.get("https://api.lolicon.app/setu/?r18=" + str(r18) + "&apikey=" + config.setu_Token)
            json_str = json.loads(res.text)
            if json_str['code'] == 401:
                user = update.effective_user.name+"：\n"

                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=user + "API接口超过调用限制（每令牌每天限制300）或API令牌被封禁"
                )
            url = json_str['data'][0]['url']
            author = json_str['data'][0]['author']
            pid = json_str['data'][0]['pid']
            title = json_str['data'][0]['title']
            is_r = "否"
            if r18 != 0:
                is_r = "是"
            user = update.effective_user.name+"：\n"

            query.bot.send_message(chat_id=update.effective_chat.id,
                                   text=user + "图片信息：\n"
                                               "作者：" + str(author)
                                        + "\n图片PID：" + str(pid)
                                        + "\n图片标题：" + str(title)
                                        + "\n是否R18：" + is_r)
            query.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=url)
        except Exception as e:
            user = update.effective_user.name+"：\n"

            query.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "服务器错误，错误原因：" + str(e) + "\n请自行访问链接：" + url
            )
        return ConversationHandler.END

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('setu', setu_input)],
        states={
            SETU: [CallbackQueryHandler(setu, pattern='^(R18|非R18)$')]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
