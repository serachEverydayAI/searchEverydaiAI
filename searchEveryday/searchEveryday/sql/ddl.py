import sqlite3


def create_table(conn, table_name, columns, index_columns):
    try:
        cursor = conn.cursor()

        # 테이블 생성 쿼리
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns}
            )
        '''
        cursor.execute(create_table_query)

        # 인덱스 생성 쿼리
        index_query = f'''
            CREATE INDEX IF NOT EXISTS {table_name}_idx 
                ON {table_name} ({index_columns})
        '''
        cursor.execute(index_query)

        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table '{table_name}': {e}")
        conn.rollback()


def create_article_crawled_data_his(conn):
    table_name = "article_crawled_data_his"
    columns = '''
                id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 자동 증가하는 고유 ID
                reg_date TEXT,                          -- 등록일자
                keyword TEXT(100),                      -- 키워드 (최대 100자)
                title TEXT(1000),                       -- 기사 제목 (최대 1000자)
                content TEXT(5000),                     -- 기사 내용 (최대 5000자)
                link TEXT(1000),                        -- 기사 링크 (최대 1000자)
                press TEXT(100),                        -- 언론사 (최대 100자)
                press_level TEXT(5),                    -- 언론사 등급
                crawling_time TEXT(17) 
        '''
    index_columns = 'reg_date, keyword'
    create_table(conn, table_name, columns, index_columns)


def create_article_crawled_data_mas(conn):
    table_name = "article_crawled_data_mas"
    columns = '''
                anchor_date TEXT(8) , 
                keyword TEXT(100) ,
                article_cnt INTEGER,
                reg_date TEXT(8),                     
                reg_time TEXT(8),                       
                update_date TEXT(8),                        
                update_time TEXT(8),
                PRIMARY KEY (anchor_date, keyword) 
    '''
    index_columns = 'anchor_date, keyword'
    create_table(conn, table_name, columns, index_columns)


def create_article_result_his(conn):
    table_name = "article_result_his"
    columns = '''
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 자동 증가하는 고유 ID
        reg_date TEXT(8), 
        keyword TEXT(100),                     -- 키워드 (최대 100자)
        title TEXT(1000),                       -- 기사 제목 (최대 1000자)
        content TEXT(5000),                     -- 기사 내용 (최대 5000자)
        link TEXT(1000),                        -- 기사 링크 (최대 1000자)
        press TEXT(100),                        -- 언론사 (최대 100자)
        press_level TEXT(5),                    -- 언론사 등급
        crawling_time TEXT(17),
        cluster_id INTEGER,
        article_cnt INTEGER
    '''
    index_columns = 'reg_date, keyword'
    create_table(conn, table_name, columns, index_columns)


def create_se_cust_info(conn):
    table_name = "se_cust_info"
    columns = '''
        cust_id VARCHAR(10) PRIMARY KEY,
        cust_nm VARCHAR(100),
        cust_birth VARCHAR(8),
        cust_telco VARCHAR(10),
        cust_hp VARCHAR(11),
        cust_email VARCHAR(100),
        cust_gender VARCHAR(2),
        cust_ssn VARCHAR(13),
        cust_ci VARCHAR(100),
        nickname VARCHAR(100),
        profile_img VARCHAR(1000),
        register_date VARCHAR(8),
        register_time VARCHAR(8),
        cust_level VARCHAR(10),
        sign_up_way VARCHAR(10),
        update_date VARCHAR(8),
        update_time VARCHAR(8)
    '''
    index_columns = 'cust_id, cust_level'
    create_table(conn, table_name, columns, index_columns)

def create_se_cust_keyword(conn):
    table_name = "se_cust_keyword"
    columns = '''
        cust_id VARCHAR(10) PRIMARY KEY,
        keyword VARCHAR(1000),
        reg_date VARCHAR(8),
        reg_time VARCHAR(8),
        update_date VARCHAR(8),
        update_time VARCHAR(8)
    '''
    index_columns = 'cust_id, keyword'
    create_table(conn, table_name, columns, index_columns)
