import sqlite3
from datetime import datetime

def execute_query(conn, query, params):
    try:
        conn.execute(query, params)
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")

def insertCrawledDataMas_WithAnchorDate_Keyword(article_cnt, keyword, day, conn):
    nowDate = datetime.now().strftime('%Y%m%d')
    nowTime = datetime.now().strftime('%H%M%S')

    query = '''
        INSERT INTO article_crawled_data_mas (anchor_date, keyword, article_cnt,
        reg_date, reg_time, update_date, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    params = (
        day,
        keyword,
        article_cnt,
        nowDate,
        nowTime,
        nowDate,
        nowTime
    )
    execute_query(conn, query, params)
    conn.commit()  # 트랜잭션 커밋
    print(f"Successfully inserted [article_crawled_data_mas]")



def insertCrawledDataHis_WithDf_Keyword(df, keyword, conn):
    nowDate = datetime.now().strftime('%Y%m%d')
    for index, row in df.iterrows():
        query = '''
              INSERT INTO article_crawled_data_his (reg_date, keyword, 
             title, content, link, press, press_level, crawling_time)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
         '''
        params = (
            nowDate,
            keyword,
            row['title'],
            row['content'],
            row['link'],
            row['press'],
            row['press_level'],
            row['crawling_time'].strftime('%Y%m%d%H%M%S%f')[:-3]  # crawling_time 포맷 yyyyMMddHHmmssSSS
        )
        execute_query(conn, query, params)
    conn.commit()  # 트랜잭션 커밋
    print(f"Successfully inserted SIZE: {len(df)} [article_crawled_data_his]")
