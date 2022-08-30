import sqlite3 as sql
from typing import List
import config

class Login:
    def insert_user(user, password):
        conn = sql.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO login (user, password) VALUES (?, ?)", user, password)
        conn.commit()
        conn.close()
    
    def get_users() -> List[tuple]:
        conn = sql.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT user, password FROM login")
        users = cur.fetchall()
        conn.close()
        return users