import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)
import requests
from module.utils.consts import cancel
from module.utils.logger import info, warning, error

SENTENCE=0

def add_sentence_plugin(dispatcher):
    # 一言-类型选择器
    def sentence_input(update: Update, _: CallbackContext) -> int:
        try:
            keyboard = [
                [
                    InlineKeyboardButton("动画", callback_data='a'),
                    InlineKeyboardButton("漫画", callback_data='b'),
                    InlineKeyboardButton("游戏", callback_data='c'),
                    InlineKeyboardButton("文学", callback_data='d'),
                ],
                [
                    InlineKeyboardButton("原创", callback_data='e'),
                    InlineKeyboardButton("网络", callback_data='f'),
                    InlineKeyboardButton("其他", callback_data='g'),
                    InlineKeyboardButton("影视", callback_data='h'),
                ],
                [
                    InlineKeyboardButton("诗词", callback_data='i'),
                    InlineKeyboardButton("网易云", callback_data='j'),
                    InlineKeyboardButton("哲学", callback_data='k'),
                    InlineKeyboardButton("抖机灵", callback_data='l'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            user = update.effective_user.name + "：\n"
            text = user + '请选择类型'
            info("一言模块：" + text)
            update.message.reply_text(
                text,
                reply_markup=reply_markup,
            )
        except:
            error("一言模块-类型选择器异常")
        return SENTENCE

    # 一言-发送句子
    def sentence(update: Update, _: CallbackContext) -> None:
        try:
            query = update.callback_query
            query.answer()
            query.delete_message()
            type = query.data
            types = {
                "a": "动画",
                "b": "漫画",
                "c": "游戏",
                "d": "文学",
                "e": "原创",
                "f": "来自网络",
                "g": "其他",
                "h": "影视",
                "i": "诗词",
                "j": "网易云",
                "k": "哲学",
                "l": "抖机灵"
            }
            type_name = types[query.data]
            try:
                res = requests.get("https://v1.hitokoto.cn?c=" + type)
                json_res = json.loads(res.text)
                s = json_res['hitokoto']
                author = json_res['from_who']
                if author == "null" or author is None:
                    author = "匿名"
                user = update.effective_user.name + "：\n"
                text = user + "类型：" + type_name + "\n" + s + "\n作者：" + author
                info("一言模块：" + text)
                query.bot.send_message(chat_id=update.effective_chat.id,
                                       text=text)
            except Exception as e:
                user = update.effective_user.name + "：\n"
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=user + "服务器错误，错误原因" + str(e)
                )
        except:
            error("一言模块：发送方法异常")
        return ConversationHandler.END

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('sentence', sentence_input)],
        states={
            SENTENCE: [CallbackQueryHandler(sentence, pattern='^(a|b|c|d|e|f|g|h|i|j|k|l)$')]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
