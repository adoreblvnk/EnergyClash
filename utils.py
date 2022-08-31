import sqlite3 as sql
from typing import List
import config
from PIL import Image
import pytesseract
import config
import cv2


class Login:
    def insert_user(self, user: str, password: str, district: str):
        conn = sql.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO login (user, password) VALUES (?, ?)", (user, password, district))
        conn.commit()
        conn.close()

    def get_users_login(self) -> List[tuple]:
        conn = sql.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT user, password FROM login")
        users = cur.fetchall()
        conn.close()
        return users

    def validate(self, name: str, password: str) -> bool:
        return (name, password) in self.get_users_login()

class OCR:
    def extract_text(img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, 0, 255)
        text = pytesseract.image_to_string(img, config="--psm 11")
        text_slice = " ".join([text]).split()
        print(text_slice)


if __name__ == "__main__":
    # print(pytesseract.pytesseract.tesseract_cmd)
    # img_path = "demo/power_supply_bill.png"

    # img = cv2.imread(img_path)
    # img = cv2.cvtColor(img, 0, 255)
    # text = pytesseract.image_to_string(img, config="--psm 11")
    # text_slice = " ".join([text]).split()
    # print(text_slice)
    pass
