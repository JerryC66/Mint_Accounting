import sqlite3
def checkDatabase():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 查询 users 表是否存在
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cur.fetchone()

    if table_exists:
        print("表 users 已成功创建")
    else:
        print("表 users 未创建")

    conn.close()

# 调用检查数据库函数
checkDatabase()