import sqlite3

from telegram import Update
from config import max_mine_stock


def sql_start_check():
    conn = sqlite3.connect('stock.db')
    try:
        create_tb_cmd = '''
           CREATE TABLE IF NOT EXISTS STOCKS
           (
           ID INT INTEGER PRIMARY KEY,
           USER_ID TEXT,
           STOCK_CODE TEXT,
           STOCK_NAME TEXT
           );
           '''
        conn.execute(create_tb_cmd)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(str(e))
        return False


def sql_insert_mine(user_id, stock_code, stock_name) -> bool:
    conn = sqlite3.connect('stock.db')
    try:
        cur = conn.cursor()
        select_count_cmd = f'''
        SELECT COUNT(ID) 
        FROM STOCKS
        WHERE USER_ID='{user_id}'
        '''
        cur.execute(select_count_cmd)
        res = cur.fetchall()
        if len(res) >= max_mine_stock:
            return False

        select_exist_cmd = f'''
        SELECT ID FROM STOCKS
        WHERE USER_ID='{user_id}' 
        AND STOCK_CODE='{stock_code}'
        '''
        cur.execute(select_exist_cmd)
        res = cur.fetchall()
        if len(res) != 0:
            return False

        insert_sql_cmd = f'''
        INSERT INTO STOCKS
        (USER_ID,STOCK_CODE,STOCK_NAME)
        VALUES 
        ('{user_id}','{stock_code}','{stock_name}')
        '''
        conn.execute(insert_sql_cmd)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def sql_select_all_mine(user_id):
    conn = sqlite3.connect('stock.db')
    try:
        cur = conn.cursor()
        insert_sql_cmd = f'''
           SELECT STOCK_CODE,STOCK_NAME 
           FROM STOCKS
           WHERE USER_ID='{user_id}'
           '''
        cur.execute(insert_sql_cmd)
        res = cur.fetchall()
        stocks = []
        for row in res:
            stocks.append([row[1], row[0]])
        conn.close()
        if len(stocks) == 0:
            return None
        return stocks
    except:
        return None


def sql_delete_mine(user_id, stock_code):
    conn = sqlite3.connect('stock.db')
    try:
        cur = conn.cursor()
        delete_sql_cmd = f'''
               DELETE FROM STOCKS
               WHERE USER_ID='{user_id}'
               AND STOCK_CODE='{stock_code}'
               '''
        cur.execute(delete_sql_cmd)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def reset_database():
    conn = sqlite3.connect('stock.db')
    try:
        cur = conn.cursor()
        reset_sql_cmd = f'''DELETE FROM STOCKS'''
        cur.execute(reset_sql_cmd)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def get_database_message():
    conn = sqlite3.connect('stock.db')
    try:
        text = ""
        cur = conn.cursor()
        sql_cmd = f'''SELECT COUNT(ID) FROM STOCKS'''
        cur.execute(sql_cmd)
        res = cur.fetchall()
        text += "数据库目前包含" + str(res[0][0]) + "条数据\n数据库内的存储状态如下（用户ID 用户存储数）：\n"
        sql_cmd = f'''SELECT COUNT(*),USER_ID FROM STOCKS GROUP BY USER_ID'''
        cur.execute(sql_cmd)
        res = cur.fetchall()
        for i in res:
            text += str(i[1]) + " " + str(i[0]) + "\n"
        conn.commit()
        conn.close()
        return text
    except Exception as e:
        return "信息获取失败：" + str(e)
