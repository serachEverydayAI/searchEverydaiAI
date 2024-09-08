from search.word_reader import read_words  # 검색 단어집 읽어오기
from search.article_crawler import crawl_articles  # 네이버 기사 검색
from search.article_clustering import cluster_articles  # 검색한 기사 분류
import pandas as pd
import os
from searchEveryday.searchEveryday.config import TEXT_FILE, CRAWLED_DATA, EXCEL_FOLDER
from searchEveryday.searchEveryday.search.article_selection import extract_max_press_level_article
from datetime import datetime


def main():
    words = read_words(os.path.join(EXCEL_FOLDER, f"{TEXT_FILE}.txt"))
    print(f'등록된 단어: {words}')

    all_articles = []
    excel_file = ''
    search_word = ''
    file_path = ''
    today_date = datetime.today().strftime('%Y%m%d')

    for index, word in enumerate(words, start=1):
        print(f"{index}: {word}")
        search_word = word
        excel_file = f"{CRAWLED_DATA}_{word}_{today_date}.xlsx"
        file_path = os.path.join(EXCEL_FOLDER, excel_file)

        if os.path.exists(file_path):
            print(f"{excel_file} 파일이 존재하므로 엑셀 파일에서 데이터를 불러옵니다.")
            df_articles = pd.read_excel(file_path)
        else:
            print(f"{excel_file} 파일이 없으므로 기사를 크롤링하여 데이터를 저장합니다.")
            df_articles = crawl_articles(search_word, excel_file)

        if df_articles.empty:
            print(f"{today_date} {words} keyword articles not found. Exiting program.")
            return 1

        all_articles.append(df_articles)

        # 3. 기사 군집화
        clustered_articles = cluster_articles(df_articles)
        # 4. 군집된 기사 정리 및 정렬
        extracted_articles = extract_max_press_level_article(clustered_articles)


if __name__ == "__main__":
    main()
