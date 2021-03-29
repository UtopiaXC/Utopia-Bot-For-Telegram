import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)
import requests
import module.utils.sql_funcs as sql_funcs
from module.utils.consts import (
    STOCK_FUNC,
    STOCK_MINE,
    STOCK_ADD_MINE,
    STOCK_DO_ADD_MINE,
    STOCK_DELETE_MINE,
    STOCK_SEARCH,
    STOCK_SELECT,
    header,
    cancel
)
from module.utils.logger import info, warning, error


def add_stock_plugin(dispatcher):
    # 股票-快速简报打印器
    def fast_list_all_mine(update, context):
        try:
            stocks = sql_funcs.sql_select_all_mine(update.effective_user.id)
            if stocks is None:
                user = update.effective_user.name + "：\n"
                text = user + "数据库中没有您的自选信息"
                warning("股票模块-快速打印简报方法：" + text)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text
                )
            else:
                text = ""
                for i in stocks:
                    try:
                        session = requests.session()
                        session.get("https://xueqiu.com/k?q=" + i[1], headers=header)
                        res = session.get("https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=" + i[1],
                                          headers=header)
                        json_str = res.json()
                        # 股票名
                        name = json_str['data']['items'][0]['quote']['name']
                        # 数据时间
                        dt = json_str['data']['items'][0]['quote']['time']
                        if dt is not None:
                            time_local = time.localtime(dt / 1000)
                            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                        # 交易状态
                        status = json_str['data']['items'][0]['market']['status']

                        # 现价
                        current = json_str['data']['items'][0]['quote']['current']
                        # 昨收
                        end_price = json_str['data']['items'][0]['quote']['last_close']
                        # 跌涨数
                        cost = 0
                        if current is not None and end_price is not None:
                            cost = current - end_price
                        # 跌涨率%
                        rate = 0
                        if cost is not None and end_price is not None and cost != 0:
                            rate = cost / end_price

                        cost = float(format(cost, ".2f"))
                        if cost > 0:
                            cost = "+" + str(cost)
                        rate = float(format(rate * 100, ".2f"))
                        if rate > 0:
                            rate = "+" + str(rate)

                        text += "%s" % dt
                        text += "（%s）\n" % status
                        text += "%s " % name
                        text += "（%s）\n" % i[1]
                        text += "现价：%s " % current
                        text += "（%s " % cost
                        text += "，%s%%）\n\n" % rate

                    except Exception as e:
                        user = update.effective_user.name + "：\n"
                        text = user + "服务器错误，错误原因：" + str(e)
                        error("股票模块-快速打印简报方法：" + text)
                        context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=text
                        )
                        return
                info("股票模块-快速打印简报方法：成功获取用户" + update.effective_user.name +
                     "的" + str(len(stocks)) + "条股票数据")
                user = update.effective_user.name + "：\n"
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=user + text
                )
        except:
            error("股票模块-快速打印简报方法异常")

    handler = CommandHandler('stock_mine', fast_list_all_mine)
    dispatcher.add_handler(handler)

    # 股票-功能选择器
    def stock_input(update: Update, _: CallbackContext) -> int:
        try:
            keyboard = [
                [
                    InlineKeyboardButton("自选", callback_data='自选'),
                    InlineKeyboardButton("搜索", callback_data='搜索'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            user = update.effective_user.name + "：\n"
            info("股票模块-方法选择器：" + update.effective_user.name + "开始了股票功能")
            update.message.reply_text(
                user + '请选择方法',
                reply_markup=reply_markup,
            )
        except:
            error("股票模块-方法选择器异常")
        return STOCK_FUNC

    # 股票-自选功能选择器
    def stock_func(update: Update, _: CallbackContext) -> int:
        try:
            query = update.callback_query
            query.answer()
            query.delete_message()
            if query.data == "自选":
                info("股票模块-功能选择器：" + update.effective_user.name + "选择了自选功能")
                keyboard = [
                    [
                        InlineKeyboardButton("添加自选", callback_data='添加自选'),
                        InlineKeyboardButton("删除自选", callback_data='删除自选'),
                    ],
                    [InlineKeyboardButton("查看自选", callback_data='查看自选')],
                    [InlineKeyboardButton("列出全部自选", callback_data='列出全部自选')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                user = update.effective_user.name + "：\n"
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=user + "请选择功能",
                    reply_markup=reply_markup,
                )
                return STOCK_MINE
            elif query.data == "搜索":
                user = update.effective_user.name + "：\n"
                info("股票模块-功能选择器：" + update.effective_user.name + "选择了搜索功能")
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=user + "请输入搜索词"
                )
                return STOCK_SEARCH
        except:
            error("股票模块-自选功能选择器异常")
            return ConversationHandler.END

    # 股票-自选股查看器
    def stock_list_mine(update: Update):
        try:
            query = update.callback_query
            user_id = update.effective_user.id
            stocks = sql_funcs.sql_select_all_mine(user_id)
            if stocks is None:
                user = update.effective_user.name + "：\n"
                warning("股票模块-自选功能-股票选择器：" + update.effective_user.name + "：数据库中无自选股")
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=user + "数据库内没有您的自选数据"
                )
                return False
            else:
                keyboard = []
                for i in stocks:
                    describe = i[0] + "（股票代码" + i[1] + "）"
                    keyboard.append([InlineKeyboardButton(describe, callback_data=i[1])])
                reply_markup = InlineKeyboardMarkup(keyboard)
                user = update.effective_user.name + "：\n"

                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=user + "请选择股票",
                    reply_markup=reply_markup,
                )
                return True
        except:
            error("股票模块-自选模块-股票选择器异常")
            return False

    # 股票-股票信息打印函数
    def display_stock(code, update: Update):
        query = update.callback_query
        try:
            session = requests.session()
            session.get("https://xueqiu.com/k?q=" + code, headers=header)
            res = session.get("https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=" + code, headers=header)
            json_str = res.json()
            # 地区
            region = json_str['data']['items'][0]['market']['region']
            # 交易状态
            status = json_str['data']['items'][0]['market']['status']
            # 时区
            time_zone = json_str['data']['items'][0]['market']['time_zone']
            # 交易市场
            exchange = json_str['data']['items'][0]['quote']['exchange']
            # 货币种类
            currency = json_str['data']['items'][0]['quote']['currency']
            # 股票名
            name = json_str['data']['items'][0]['quote']['name']
            # 数据时间
            dt = json_str['data']['items'][0]['quote']['time']
            if dt is not None:
                time_local = time.localtime(dt / 1000)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            # 现价
            current = json_str['data']['items'][0]['quote']['current']
            # 今开
            start_price = json_str['data']['items'][0]['quote']['open']
            # 昨收
            end_price = json_str['data']['items'][0]['quote']['last_close']
            # 跌涨数
            cost = 0
            if current is not None and end_price is not None:
                cost = current - end_price
            # 跌涨率%
            rate = 0
            if cost is not None and end_price is not None and cost != 0:
                rate = cost / end_price

            cost = float(format(cost, ".2f"))
            if cost > 0:
                cost = "+" + str(cost)
            rate = float(format(rate * 100, ".2f"))
            if rate > 0:
                rate = "+" + str(rate)
            # 最高
            high = json_str['data']['items'][0]['quote']['high']
            # 最低
            low = json_str['data']['items'][0]['quote']['low']
            # 成交量（万手）
            deal = json_str['data']['items'][0]['quote']['volume']
            if deal is not None:
                deal = format(float(format(deal / 10000, ".2f")), ",")
            # 成交额（万元）
            amount = json_str['data']['items'][0]['quote']['amount']
            if amount is not None:
                amount = format(int(format(amount / 10000, ".0f")), ",")
            # 换手
            turnover_rate = json_str['data']['items'][0]['quote']['turnover_rate']
            # 振幅
            amplitude = json_str['data']['items'][0]['quote']['amplitude']
            # 市值（万元）
            total_price = json_str['data']['items'][0]['quote']['market_capital']
            if total_price is not None:
                total_price = format(int(format(total_price / 10000, ".0f")), ",")
            # 总股本（万元）
            total_shares = json_str['data']['items'][0]['quote']['total_shares']
            if total_price is not None:
                total_shares = format(int(format(total_shares / 10000, ".0f")), ",")
            text = "股票名称：%s\n" % name
            text += "股票代码：%s\n" % code
            text += "地区：%s\n" % region
            text += "时区：%s\n" % time_zone
            text += "交易市场：%s\n" % exchange
            text += "货币种类：%s\n" % currency
            text += "交易状态：%s\n" % status
            text += "数据时间（当地）：%s\n" % dt
            text += "现价：%s\n" % current
            text += "今开：%s\n" % start_price
            text += "昨收：%s\n" % end_price
            text += "跌涨：%s\n" % cost
            text += "跌涨率：%s%%\n" % rate
            text += "最高：%s\n" % high
            text += "最低：%s\n" % low
            text += "成交量：%s万手\n" % deal
            text += "成交额：%s万\n" % amount
            text += "换手：%s%%\n" % turnover_rate
            text += "振幅：%s%%\n" % amplitude
            text += "市值：%s万\n" % total_price
            text += "总股本：%s万" % total_shares
            user = update.effective_user.name + "：\n"
            info("股票模块-自选股-自选股具体信息：用户" + update.effective_user.name +
                 "打印了一条股票具体信息，股票代码：" + code)
            query.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + text
            )
        except Exception as e:
            user = update.effective_user.name + "：\n"
            text = user + "服务器错误，错误原因：" + str(e)
            error("股票模块-自选股-自选股具体信息：" + text)
            query.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )

    # 股票-自选功能选择器
    def stock_mine(update: Update, _: CallbackContext) -> int:
        try:
            query = update.callback_query
            query.answer()
            query.delete_message()
            if query.data == "添加自选":
                user = update.effective_user.name + "：\n"
                info("股票模块-自选股功能-自选股功能选择处理器：用户"+
                     update.effective_user.name+
                     "选择添加一条自选")
                query.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=user + "请输入搜索词"
                )
                return STOCK_ADD_MINE
            elif query.data == "删除自选":
                info("股票模块-自选股功能-自选股功能选择处理器：用户" +
                     update.effective_user.name +
                     "选择删除一条自选")
                if not stock_list_mine(update):
                    return ConversationHandler.END
                else:
                    return STOCK_DELETE_MINE
            elif query.data == "查看自选":
                info("股票模块-自选股功能-自选股功能选择处理器：用户" +
                     update.effective_user.name +
                     "选择查看全部自选")
                if not stock_list_mine(update):
                    return ConversationHandler.END
                else:
                    return STOCK_SELECT
            elif query.data == "列出全部自选":
                info("股票模块-自选股功能-自选股功能选择处理器：用户" +
                     update.effective_user.name +
                     "选择列出全部自选简报")
                stocks = sql_funcs.sql_select_all_mine(update.effective_user.id)
                if stocks is None:
                    user = update.effective_user.name + "：\n"

                    query.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=user + "数据库中没有您的自选信息"
                    )
                else:
                    stocks = sql_funcs.sql_select_all_mine(update.effective_user.id)
                    if stocks is None:
                        user = update.effective_user.name + "：\n"

                        query.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=user + "数据库中没有您的自选信息"
                        )
                    else:
                        text = ""
                        for i in stocks:
                            try:
                                session = requests.session()
                                session.get("https://xueqiu.com/k?q=" + i[1], headers=header)
                                res = session.get("https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=" + i[1],
                                                  headers=header)
                                json_str = res.json()
                                # 股票名
                                name = json_str['data']['items'][0]['quote']['name']
                                # 数据时间
                                dt = json_str['data']['items'][0]['quote']['time']
                                if dt is not None:
                                    time_local = time.localtime(dt / 1000)
                                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                                # 交易状态
                                status = json_str['data']['items'][0]['market']['status']

                                # 现价
                                current = json_str['data']['items'][0]['quote']['current']
                                # 昨收
                                end_price = json_str['data']['items'][0]['quote']['last_close']
                                # 跌涨数
                                cost = 0
                                if current is not None and end_price is not None:
                                    cost = current - end_price
                                # 跌涨率%
                                rate = 0
                                if cost is not None and end_price is not None and cost != 0:
                                    rate = cost / end_price

                                cost = float(format(cost, ".2f"))
                                if cost > 0:
                                    cost = "+" + str(cost)
                                rate = float(format(rate * 100, ".2f"))
                                if rate > 0:
                                    rate = "+" + str(rate)

                                text += "%s" % dt
                                text += "（%s）\n" % status
                                text += "%s " % name
                                text += "（%s）\n" % i[1]
                                text += "现价：%s " % current
                                text += "（%s " % cost
                                text += "，%s%%）\n\n" % rate

                            except Exception as e:
                                user = update.effective_user.name + "：\n"

                                query.bot.send_message(
                                    chat_id=update.effective_chat.id,
                                    text=user + "服务器错误，错误原因：" + str(e)
                                )
                                return ConversationHandler.END

                        user = update.effective_user.name + "：\n"
                        query.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=user + text
                        )
                    return ConversationHandler.END
        except:
            error("股票模块-自选股功能-自选股功能选择处理器异常")
            return ConversationHandler.END

    # 股票-股票查找器
    def search_func(update: Update):
        try:
            key = update.message.text
            session = requests.session()
            session.get("https://xueqiu.com/k?q=" + key, headers=header)
            res = session.get("https://xueqiu.com/query/v1/search/web/stock.json?q=" + key, headers=header)
            json_str = res.json()
            res = json_str['list']
            flag = 0
            keyboard = []
            for i in res:
                flag += 1
                if flag > 5:
                    break
                describe = i['name'] + "（股票代码" + i['code'] + "）"
                keyboard.append([InlineKeyboardButton(describe, callback_data=i['code'])])
            if json_str['count'] == 0:
                user = update.effective_user.name + "：\n"

                update.message.reply_text(
                    text=user + "无搜索结果"
                )
                return ConversationHandler.END
            text = "获取到的结果共%s个\n请选择一个进行查看\n" % json_str['count']
            if json_str['count'] > 5:
                text += "搜索结果过多，仅显示前五条结果"
            reply_markup = InlineKeyboardMarkup(keyboard)
            user = update.effective_user.name + "：\n"

            update.message.reply_text(
                text=user + text,
                reply_markup=reply_markup,
            )
        except Exception as e:
            user = update.effective_user.name + "：\n"

            update.message.reply_text(
                text=user + "服务器错误，错误原因：" + str(e)
            )

    # 股票-自选股添加选择器
    def add_mine(update: Update, _: CallbackContext) -> int:
        info("用户"+update.effective_user.name+"选择了添加自选")
        search_func(update)
        return STOCK_DO_ADD_MINE

    # 股票-自选股添加器
    def do_add_mine(update: Update, _: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        query.delete_message()
        code = query.data
        info("用户" + update.effective_user.name + "添加了一条自选，代码为：" +code)
        user_id = update.effective_user.id
        session = requests.session()
        session.get("https://xueqiu.com/k?q=" + code, headers=header)
        res = session.get("https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=" + code, headers=header)
        json_str = res.json()
        name = json_str['data']['items'][0]['quote']['name']
        if sql_funcs.sql_insert_mine(user_id, code, name):
            user = update.effective_user.name + "：\n"
            info("用户" + update.effective_user.name + "添加了一条自选成功，代码为：" + code)
            query.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "添加成功"
            )
        else:
            user = update.effective_user.name + "：\n"
            warning("用户" + update.effective_user.name + "添加自选失败，代码为：" + code)
            query.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "添加失败"
            )
        return ConversationHandler.END

    # 股票-自选股删除器
    def do_delete_mine(update: Update, _: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        query.delete_message()
        code = query.data
        info("用户" + update.effective_user.name + "删除了一条自选，代码为：" + code)
        user_id = update.effective_user.id
        if sql_funcs.sql_delete_mine(user_id, code):
            user = update.effective_user.name + "：\n"
            info("用户" + update.effective_user.name + "删除了一条自选成功，代码为：" + code)
            query.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "删除成功"
            )
        else:
            user = update.effective_user.name + "：\n"
            info("用户" + update.effective_user.name + "删除了一条自选失败，代码为：" + code)
            query.bot.send_message(
                chat_id=update.effective_chat.id,
                text=user + "删除失败"
            )
        return ConversationHandler.END

    # 股票-搜索功能
    def stock_search(update: Update, _: CallbackContext) -> int:
        search_func(update)
        return STOCK_SELECT

    # 股票-查看搜索结果股票信息
    def stock_select(update: Update, _: CallbackContext) -> int:
        query = update.callback_query
        query.answer()
        query.delete_message()
        code = query.data
        display_stock(code, update)
        return ConversationHandler.END

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('stock', stock_input)],
        states={
            STOCK_FUNC: [CallbackQueryHandler(stock_func, pattern='^(自选|搜索)$')],
            STOCK_SEARCH: [MessageHandler(Filters.text, stock_search)],
            STOCK_MINE: [CallbackQueryHandler(stock_mine)],
            STOCK_SELECT: [CallbackQueryHandler(stock_select)],
            STOCK_ADD_MINE: [MessageHandler(Filters.text, add_mine)],
            STOCK_DO_ADD_MINE: [CallbackQueryHandler(do_add_mine)],
            STOCK_DELETE_MINE: [CallbackQueryHandler(do_delete_mine)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
