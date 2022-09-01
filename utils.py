import os
import re
import sqlite3 as sql
from typing import Dict, List

import cv2
import pytesseract
from PIL import Image

import config


class Database:
    def insert_user(self, user: str, password: str, district: str):
        conn = sql.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO login (user, password, district) VALUES (?, ?, ?)", (user, password, district))
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
    def tesseract_output(self, img_path: str) -> Dict[str, List]:
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, 0, 255)
        return pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config="--psm 11")

    def extract_text(self, tesseract_data: Dict[str, List]) -> List[str]:
        text_slice = tesseract_data["text"]
        return [word for word in text_slice if word.strip()]

    # returns maximum power consumption, typically the most accurate.
    def extract_power_consumption(self, text_slice: List[str]) -> str:
        kwh_list = []
        for idx, word in enumerate(text_slice):
            # 2 cases:
            # case_1: <number>kWh
            # case_2: <number> kWh
            # we will separate & validate these 2 cases separately.
            case_1 = re.findall(r"(?i)^\d+kwh", word)
            case_2 = re.findall(r"(?i)^kwh", word)
            if case_1:
                try:
                    kwh = float(word[:-3])
                    kwh_list.append(kwh)
                except ValueError:
                    continue
            if case_2:
                try:
                    kwh = float(text_slice[idx-1])
                    kwh_list.append(kwh)
                except ValueError:
                    continue
        return str(max(kwh_list)) if kwh_list else ""
    
    # draw boxes around detected text & returns output filepath.
    def draw_boxes(self, img_path: str, d: Dict[str, List]):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, 0, 255)
        # d: tesseract data
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (76, 87, 214), 2)
        filename, file_extension = os.path.splitext(img_path)
        img_output_path = f"{filename}_output{file_extension}"
        cv2.imwrite(img_output_path, img)
        return img_output_path
