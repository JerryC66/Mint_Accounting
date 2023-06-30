import sqlite3

def buildDatabase():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS users(
    user_id   INT    NOT NULL ,
    username    TEXT    NOT NULL,
    password    TEXT    NOT NULL,
    PRIMARY KEY (user_id));
       """)
    
    conn.commit()
    conn.close()

buildDatabase()
    

