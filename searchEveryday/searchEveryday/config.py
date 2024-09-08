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
    def __init__(self, db_path):
        self.db_path = db_path
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

def create_articles_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    link TEXT,
                    press TEXT,
                    press_level TEXT,
                    crawling_time TEXT
                )
                ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()

def save_articles_to_db(df_articles, search_word, conn):
    try:
        cursor = conn.cursor()
        for _, row in df_articles.iterrows():
            cursor.execute('''
            INSERT INTO articles (search_word, article_title, article_content) VALUES (?, ?, ?)
            ''', (search_word, row['title'], row['content']))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving articles: {e}")
        conn.rollback()

def read_articles_from_db(search_word, conn):
    try:
        query = "SELECT * FROM articles WHERE search_word = ?"
        df_articles = pd.read_sql_query(query, conn, params=(search_word,))
        return df_articles
    except sqlite3.Error as e:
        print(f"Error reading articles: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error
