import os
import sqlite3
import pandas as pd
from datetime import datetime

API_KEY = 'your-chatgpt-api-key'
NUM_CLUSTERS = 5

TEXT_FILE = "keyword"
CRAWLED_DATA = "crwaledData"
EXCEL_FOLDER = os.path.join(os.getcwd(), 'excelfiles')
RESULT_ARTICLE = "result_article"

DB_PATH = 'db.sqlite3'

class DatabaseConnection:
    def __init__(self, db_name):
        # 현재 스크립트의 디렉토리 경로를 가져옵니다.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 상위 폴더 경로를 가져옵니다.
        parent_dir = os.path.dirname(current_dir)
        # 상위 폴더에 데이터베이스 파일 경로를 설정합니다.
        self.db_path = os.path.join(parent_dir, db_name)
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            return self.conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
