import sqlite3


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
