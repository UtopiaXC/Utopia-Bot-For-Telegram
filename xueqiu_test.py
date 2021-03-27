import time

import requests
import urllib

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"
}

name = input("请输入搜索关键字：")

session = requests.session()
session.get("https://xueqiu.com/k?q=" + name, headers=header)
res = session.get("https://xueqiu.com/query/v1/search/web/stock.json?q=" + name, headers=header)
json_str = res.json()
res = json_str['list']
print("获取到的结果共" + str(json_str['count']))
if json_str['count'] > 5:
    print("搜索结果过多，仅显示前五条结果")
flag = 0
for i in res:
    flag += 1
    if flag > 5:
        break
    print("搜索结果%d：" % flag)
    # 代码
    code = i['code']
    # 名称
    name = i['name']
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
    # 数据时间
    dt = json_str['data']['items'][0]['quote']['time']
    if dt != None:
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
    if current != None and end_price != None:
        cost = current - end_price
    # 跌涨率%
    rate = 0
    if cost != None and end_price != None and cost != 0:
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
    if deal != None:
        deal = format(float(format(deal / 10000, ".2f")), ",")
    # 成交额（万元）
    amount = json_str['data']['items'][0]['quote']['amount']
    if amount != None:
        amount = format(int(format(amount / 10000, ".0f")), ",")
    # 换手
    turnover_rate = json_str['data']['items'][0]['quote']['turnover_rate']
    # 振幅
    amplitude = json_str['data']['items'][0]['quote']['amplitude']
    # 市值（万元）
    total_price = json_str['data']['items'][0]['quote']['market_capital']
    if total_price != None:
        total_price = format(int(format(total_price / 10000, ".0f")), ",")
    # 总股本（万元）
    total_shares = json_str['data']['items'][0]['quote']['total_shares']
    if total_price != None:
        total_shares = format(int(format(total_shares / 10000, ".0f")), ",")
    print("股票名称：%s" % name)
    print("股票代码：%s" % code)
    print("地区：%s" % region)
    print("时区：%s" % time_zone)
    print("交易市场：%s" % exchange)
    print("货币种类：%s" % currency)
    print("交易状态：%s" % status)
    print("数据时间（当地）：%s" % dt)
    print("现价：%s" % current)
    print("今开：%s" % start_price)
    print("昨收：%s" % end_price)
    print("跌涨：%s" % cost)
    print("跌涨率：%s%%" % rate)
    print("最高：%s" % high)
    print("最低：%s" % low)
    print("成交量：%s万手" % deal)
    print("成交额：%s万" % amount)
    print("换手：%s%%" % turnover_rate)
    print("振幅：%s%%" % amplitude)
    print("市值：%s万" % total_price)
    print("总股本：%s万\n" % total_shares)
