from search.word_reader import read_words  # 검색 단어집 읽어오기
from search.article_crawler import crawl_articles  # 네이버 기사 검색
from search.article_clustering import cluster_articles  # 검색한 기사 분류
import pandas as pd
import os
from searchEveryday.searchEveryday.config import TEXT_FILE, CRAWLED_DATA, EXCEL_FOLDER, \
    DatabaseConnection, DB_PATH
from searchEveryday.searchEveryday.search.article_selection import extract_max_press_level_article
from datetime import datetime

from searchEveryday.searchEveryday.sql.ddl import create_article_crawled_data_his, create_article_result_his, \
    create_article_crawled_data_mas, create_se_cust_info, create_se_cust_keyword
from searchEveryday.searchEveryday.sql.select import getCrawledDataMas_WithAnchorDate_Keyword, \
    getCrawledDataHis_WithAnchorDate_Keyword


def article_main():
    words = read_words(os.path.join(EXCEL_FOLDER, f"{TEXT_FILE}.txt"))
    print(f'등록된 단어 목록: {words}')
    today_date = datetime.today().strftime('%Y%m%d')

    with DatabaseConnection(DB_PATH) as conn:

        for index, word in enumerate(words, start=1):
            print(f"{index}: {word}")
            search_word = word

            filename = f"{CRAWLED_DATA}_{word}_{today_date}"
            file_path = os.path.join(EXCEL_FOLDER, filename)

            # 함수 호출
            df_articles = getCrawledDataMas_WithAnchorDate_Keyword(today_date, word, conn)

            # 결과가 비어 있는지 확인
            if not df_articles.empty:
                print(f"{today_date}: 저장된 {filename} 키워드가 있습니다. 기존 데이터를 불러옵니다.")
                #df_his_articles = pd.read_excel(file_path)
                df_his_articles = getCrawledDataHis_WithAnchorDate_Keyword(today_date, word, conn)
            else:
                print(f"{today_date}: 저장된 {filename} 키워드가 없습니다. 새로운 기사를 크롤링하여 데이터를 저장합니다.")
                #print(df_articles.iloc[0])  # 첫 번째 행(기사)을 출력

                df_his_articles = crawl_articles(search_word, filename, today_date, conn)

            if df_his_articles.empty:
                print(f"{today_date} {word} keyword articles not found. Exiting program.")
                continue

            # 3. 기사 군집화
            clustered_articles = cluster_articles(df_his_articles)
            # 4. 군집된 기사 정리 및 정렬
            extracted_articles = extract_max_press_level_article(clustered_articles, word, conn)

def server_init():
    """ 신규 테이블 생성  """
    with DatabaseConnection(DB_PATH) as conn:
        create_article_crawled_data_his(conn)
        create_article_crawled_data_mas(conn)
        create_article_result_his(conn)
        create_se_cust_info(conn)
        create_se_cust_keyword(conn)


if __name__ == "__main__":
    article_main()
    #server_init()
