from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler, MessageHandler, Filters,
)
from .utils.consts import cancel
from .utils.logger import info, warning, error, compress_file
from .utils.sql_funcs import get_database_message, reset_database
from config import admin_id

ADMIN_SELECT, \
DATABASE, \
LOG, \
DELETE_DATABASE, \
    = range(4)


def add_admin_plugin(dispatcher):
    # 管理员功能选择
    def admin_select(update: Update, _: CallbackContext) -> int:
        try:
            id = update.effective_user.id
            if str(id) not in admin_id:
                user = update.effective_user.name
                user_id = str(update.effective_user.id)
                user_name = str(update.effective_user.name)
                log_text = user_name + "(" + user_id + ")" + "非管理员用户请求访问管理功能"
                warning("管理员模块" + log_text)
                text = user + "：\n" + "您不是管理员，没有本指令权限！\n" \
                                      "如果您是管理员，请先将您的ID添加如配置文件"
                update.message.reply_text(text)
                return ConversationHandler.END
            keyboard = [
                [InlineKeyboardButton("数据库", callback_data='数据库')],
                [InlineKeyboardButton("日志", callback_data='日志')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            user = update.effective_user.name
            text = user + "：\n" + '请选择管理功能'
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" + "一名管理员选择了管理员功能"
            info("管理员模块：" + log_text)
            update.message.reply_text(
                text,
                reply_markup=reply_markup,
            )
            return ADMIN_SELECT
        except Exception as e:
            error("管理员模块异常：" + str(repr(e)))

    # 管理员-接收选择结果
    def admin(update: Update, _: CallbackContext) -> None:
        try:
            query = update.callback_query
            query.answer()
            query.delete_message()
            type = query.data
            if type == "数据库":
                keyboard = [
                    [InlineKeyboardButton("获取数据库信息", callback_data='获取数据库信息')],
                    [InlineKeyboardButton("重置数据库", callback_data='重置数据库')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                user = update.effective_user.name
                text = user + "：\n" + '请选择数据库管理功能'
                user_id = str(update.effective_user.id)
                user_name = str(update.effective_user.name)
                log_text = user_name + "(" + user_id + ")" + "一名管理员选择了数据库管理功能"
                info("管理员模块：" +log_text)
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text,
                    reply_markup=reply_markup,
                )
                return DATABASE
            elif type == "日志":
                keyboard = [
                    [InlineKeyboardButton("完整日志", callback_data='完整日志')],
                    [InlineKeyboardButton("信息日志", callback_data='信息日志')],
                    [InlineKeyboardButton("警告日志", callback_data='警告日志')],
                    [InlineKeyboardButton("错误日志", callback_data='错误日志')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                user = update.effective_user.name
                text = user + "：\n" + '请选择日志类型功能'
                user_id = str(update.effective_user.id)
                user_name = str(update.effective_user.name)
                log_text = user_name + "(" + user_id + ")" + "一名管理员选择了日志管理功能"
                info("管理员模块：" + log_text)
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text,
                    reply_markup=reply_markup,
                )
                return LOG


        except Exception as e:
            error("管理员模块：异常：" + str(repr(e)))
            return ConversationHandler.END

    # 管理员-日志管理模块
    def log_management(update: Update, _: CallbackContext):
        try:
            query = update.callback_query
            query.answer()
            query.delete_message()
            type = query.data
            if type == "完整日志":
                compress_file("logs/logs_full.zip", "logs/full")
                file = open("logs/logs_full.zip", "rb")
                query.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=file
                )
            elif type == "信息日志":
                compress_file("logs/logs_info.zip", "logs/info")
                file = open("logs/logs_info.zip", "rb")
                query.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=file
                )
            elif type == "警告日志":
                compress_file("logs/logs_warning.zip", "logs/warning")
                file = open("logs/logs_warning.zip", "rb")
                query.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=file
                )
            elif type == "错误日志":
                compress_file("logs/logs_error.zip", "logs/error")
                file = open("logs/logs_error.zip", "rb")
                query.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=file
                )
            return ConversationHandler.END
        except Exception as e:
            error("日志管理模块异常：" + str(repr(e)))
            return ConversationHandler.END

    # 管理员-数据库操作模块
    def db_management_select(update: Update, _: CallbackContext):
        try:
            query = update.callback_query
            query.answer()
            query.delete_message()
            type = query.data
            if type == "获取数据库信息":
                user = update.effective_user.name
                user_id = str(update.effective_user.id)
                user_name = str(update.effective_user.name)
                log_text = user_name + "(" + user_id + ")" + "一名管理员获取了数据库信息"
                info("管理员模块：" + log_text)
                text = user + "：\n" + get_database_message()
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text
                )
                return ConversationHandler.END
            elif type == "重置数据库":
                user = update.effective_user.name
                user_id = str(update.effective_user.id)
                user_name = str(update.effective_user.name)
                log_text = user_name + "(" + user_id + ")" + "选择了重置数据库，进入验证阶段"
                info("管理员模块：" + log_text)
                text = user + "：\n请输入您的ID来确认重置数据库"
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text
                )
            return DELETE_DATABASE
        except Exception as e:
            error("管理员模块：数据库管理模块-操作选择接收异常：" + str(repr(e)))
            return ConversationHandler.END

    def reset_db(update: Update, _: CallbackContext):
        input = update.message.text
        query = update.callback_query
        if str(input) != str(update.effective_user.id) or str(update.effective_user.id) not in admin_id:
            user = update.effective_user.name
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" + "在执行数据库重置时输入了错误的ID，执行被取消"
            info("管理员模块：" + log_text)
            text = user + "：\n" + "您输入的ID有误或无管理员权限，数据库的重置已取消"
            update.message.reply_text(
                text=text
            )
            return ConversationHandler.END
        if not reset_database():
            user = update.effective_user.name
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" + "在执行数据库重置时发生了数据库错误，数据库重置失败"
            info("管理员模块：" + log_text)
            text = user + "：\n" + "在执行数据库重置时发生了数据库错误，数据库重置失败"
            update.message.reply_text(
                text=text
            )
        else:
            user = update.effective_user.name
            user_id = str(update.effective_user.id)
            user_name = str(update.effective_user.name)
            log_text = user_name + "(" + user_id + ")" + "重置了数据库"
            info("管理员模块：" + log_text)
            text = user + "：\n" + "数据库重置成功"
            update.message.reply_text(
                text=text
            )
        return ConversationHandler.END

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', admin_select)],
        states={
            ADMIN_SELECT: [CallbackQueryHandler(admin, pattern='^(数据库|日志)$')],
            LOG: [CallbackQueryHandler(log_management, pattern='^(完整日志|信息日志|警告日志|错误日志)$')],
            DATABASE: [CallbackQueryHandler(db_management_select, pattern='^(获取数据库信息|重置数据库)$')],
            DELETE_DATABASE: [MessageHandler(Filters.text, reset_db)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
