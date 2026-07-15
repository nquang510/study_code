import pymysql

def get_connection():
    conn = pymysql.connect(
        host='localhost',
        port=3307,
        user='root',
        password='',
        database='shop',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    return conn