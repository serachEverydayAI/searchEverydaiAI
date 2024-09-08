from search.word_reader import read_words  # 검색 단어집 읽어오기
from search.article_crawler import crawl_articles  # 네이버 기사 검색
from search.article_clustering import cluster_articles  # 검색한 기사 분류
#from search.article_summary import summarize_article  # 검색한 기사 요약
import os
import pandas as pd
from searchEveryday.searchEveryday.search.article_selection import extract_max_press_level_article
from datetime import datetime


text_file = "keyword"
crwaled_data = "crwaledData"

def main():
    words = read_words(text_file + '.txt')
    print(f'등록된 단어: {words}')

    all_articles = []
    excel_file_path = ''
    searchWord = ''
    today_date = datetime.today().strftime('%Y%m%d')

    for index, word in enumerate(words, start=1):
        print(f"{index}: {word}")
        searchWord = word
        excel_file_path = f"{crwaled_data}_{word}_{today_date}.xlsx"

    if os.path.exists(excel_file_path):
        print(f"{excel_file_path} 파일이 존재하므로 엑셀 파일에서 데이터를 불러옵니다.")
        df_articles = pd.read_excel(excel_file_path)
    else:
        print(f"{excel_file_path} 파일이 없으므로 기사를 크롤링하여 데이터를 저장합니다.")
        df_articles = crawl_articles(searchWord, excel_file_path)

    if df_articles.empty:
        print(f"{today_date} {words} keyword articles not found. Exiting program.")
        return 1

    all_articles.append(df_articles)

    if len(all_articles[0]) == 1:
        print(f"{today_date} {words} keyword article is one. Nothing to cluseter.")
        return 1

    combined_df = pd.concat(all_articles, ignore_index=True)
    #print("최종 기사 데이터:", combined_df)
    # 3. 검색한 기사 분류
    clustered_articles = cluster_articles(df_articles)

    # row 생략 없이 출력
    pd.set_option('display.max_rows', None)
    # col 생략 없이 출력
    pd.set_option('display.max_columns', None)
    print(f'clustered_articles: {clustered_articles}')

    extracted_articles = extract_max_press_level_article(clustered_articles)

    #print(f"\nREUSLT: {extracted_articles}")


    # 4. 검색한 기사 요약
    # for cluster_id, articles in clustered_articles.items():
    #     print(f"\nCluster {cluster_id + 1}")
    #     for article in articles:
    #         summary = summarize_article(article['summary'])
    #         print(f"\nTitle: {article['title']}\nLink: {article['link']}\nSummary: {summary}")


if __name__ == "__main__":
    main()
