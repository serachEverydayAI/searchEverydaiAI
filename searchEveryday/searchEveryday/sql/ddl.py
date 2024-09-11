import sqlite3

def create_article_crawled_data_his(conn):
    table_name = "article_crawled_data_his"
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 자동 증가하는 고유 ID
                reg_date TEXT,                          -- 등록일자
                keyword TEXT(100),                      -- 키워드 (최대 100자)
                title TEXT(1000),                       -- 기사 제목 (최대 1000자)
                content TEXT(5000),                     -- 기사 내용 (최대 5000자)
                link TEXT(1000),                        -- 기사 링크 (최대 1000자)
                press TEXT(100),                        -- 언론사 (최대 100자)
                press_level TEXT(5),                    -- 언론사 등급
                crawling_time TEXT(17) 
            )
        ''')
        cursor.execute(f'''
            CREATE INDEX IF NOT EXISTS {table_name}_idx_1 
                ON {table_name} (reg_date, keyword)
            ''')
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table '{table_name}': {e}")
        conn.rollback()

def create_article_crawled_data_mas(conn):
    table_name = "article_crawled_data_mas"
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                anchor_date TEXT(8) , 
                keyword TEXT(100) ,
                article_cnt INTEGER,
                reg_date TEXT(8),                     
                reg_time TEXT(8),                       
                update_date TEXT(8),                        
                update_time TEXT(8),
                PRIMARY KEY (anchor_date, keyword)         
            )
        ''')
        cursor.execute(f'''
            CREATE INDEX IF NOT EXISTS {table_name}_idx_1 
                ON {table_name} (anchor_date, keyword)
            ''')
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table '{table_name}': {e}")
        conn.rollback()


def create_article_result_his(conn):
    table_name = "article_result_his"
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 자동 증가하는 고유 ID
                reg_date TEXT(8) , 
                keyword TEXT(100) ,                     -- 키워드 (최대 100자)
                title TEXT(1000),                       -- 기사 제목 (최대 1000자)
                content TEXT(5000),                     -- 기사 내용 (최대 5000자)
                link TEXT(1000),                        -- 기사 링크 (최대 1000자)
                press TEXT(100),                        -- 언론사 (최대 100자)
                press_level TEXT(5),                    -- 언론사 등급
                crawling_time TEXT(17),
                cluster_id INTEGER,
                article_cnt INTEGER
            )
        ''')
        cursor.execute(f'''
            CREATE INDEX IF NOT EXISTS {table_name}_idx_1 
                ON {table_name} (reg_date, keyword)
            ''')
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table '{table_name}': {e}")
        conn.rollback()