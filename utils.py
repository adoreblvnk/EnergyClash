import sqlite3 as sql
from typing import List
import config


class Login:
    def insert_user(self, user: str, password: str):
        conn = sql.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO login (user, password) VALUES (?, ?)", (user, password))
        conn.commit()
        conn.close()

    def get_users(self) -> List[tuple]:
        conn = sql.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT user, password FROM login")
        users = cur.fetchall()
        conn.close()
        return users

    def validate(self, name: str, password: str) -> bool:
        input_tuple: tuple = (name, password)
        user_list = self.get_users()
        return input_tuple in user_list
