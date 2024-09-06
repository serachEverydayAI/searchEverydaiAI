from search.word_reader import read_words  # 검색 단어집 읽어오기
from search.article_crawler import crawl_articles  # 네이버 기사 검색
from search.article_clustering import cluster_articles  # 검색한 기사 분류
#from search.article_summary import summarize_article  # 검색한 기사 요약
from searchEveryday.searchEveryday.config import NUM_CLUSTERS


def main():
    # 1. 단어집에서 단어 읽어오기
    words = read_words('word_list.txt')
    print(f'등록된 단어: {words}')
    # 2. 단어로 기사 검색
    all_articles = []
    for index, word in enumerate(words, start=1):
        print(f"{index}: {word}")
        df_articles = crawl_articles(word)

    # 3. 검색한 기사 분류
    clustered_articles = cluster_articles(df_articles)

    # 4. 검색한 기사 요약
    # for cluster_id, articles in clustered_articles.items():
    #     print(f"\nCluster {cluster_id + 1}")
    #     for article in articles:
    #         summary = summarize_article(article['summary'])
    #         print(f"\nTitle: {article['title']}\nLink: {article['link']}\nSummary: {summary}")


if __name__ == "__main__":
    main()
