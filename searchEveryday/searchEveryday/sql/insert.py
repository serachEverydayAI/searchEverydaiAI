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
            row['crawling_time']
        )
        execute_query(conn, query, params)
    conn.commit()  # 트랜잭션 커밋
    print(f"Successfully inserted SIZE: {len(df)} [article_crawled_data_his]")

def insertResultHis_WithDf_Keyword(df, keyword, conn):
    nowDate = datetime.now().strftime('%Y%m%d')
    for index, row in df.iterrows():
        query = '''
              INSERT INTO article_result_his (reg_date, keyword, 
             title, content, link, press, press_level, crawling_time, cluster_id, article_cnt)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
         '''
        params = (
            nowDate,
            keyword,
            row['title'],
            row['content'],
            row['link'],
            row['press'],
            row['press_level'],
            row['crawling_time'],
            row['cluster_id'],
            row['count']
        )
        execute_query(conn, query, params)
    conn.commit()  # 트랜잭션 커밋
    print(f"Successfully inserted [article_result_his]")


def get_next_cust_id(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(cust_id) FROM se_cust_info')
    result = cursor.fetchone()[0]

    # 처음 삽입되는 경우
    if result is None:
        return '0100000001'

    # 최대값이 존재하는 경우, 정수로 변환하여 1 증가
    max_id = int(result)
    next_id = max_id + 1

    # 포맷을 맞추기 위해 문자열로 변환
    return f'{next_id:010d}'  # 10자리 문자열로 포맷팅

def insertSeCustInfo(conn, cust_nm, cust_birth, cust_telco, cust_hp, cust_email, cust_gender, cust_ssn, cust_ci, nickname, profile_img,
                        cust_level, sign_up_way):
    nowDate = datetime.now().strftime('%Y%m%d')
    nowTime = datetime.now().strftime('%H%M%S')

    cust_id = get_next_cust_id(conn)

    query = '''
        INSERT INTO se_cust_info (
            cust_id, cust_nm, cust_birth, cust_telco, cust_hp, cust_email,
            cust_gender, cust_ssn, cust_ci,  nickname,
            profile_img, register_date, register_time, cust_level, sign_up_way,
            update_date, update_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    params = (
        cust_id, cust_nm, cust_birth, cust_telco, cust_hp, cust_email,
        cust_gender, cust_ssn, cust_ci, nickname, profile_img, nowDate, nowTime, cust_level, sign_up_way,
        nowDate, nowTime
    )
    execute_query(conn, query, params)
    conn.commit()
    print(f"Inserted new record CUST_ID: {cust_id} {nickname}")
