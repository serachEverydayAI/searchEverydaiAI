import pandas as pd
import os
from searchEveryday.searchEveryday.config import EXCEL_FOLDER, RESULT_ARTICLE
from searchEveryday.searchEveryday.sql.insert import insertResultHis_WithDf_Keyword


def extract_max_press_level_article(cluster_data, keyword, conn):
    max_press_articles = []
    cluster_counts = {}
    for cluster, articles in cluster_data.items():
        cluster_counts[cluster] = len(articles)
        # 각 군집의 기사 중 'press_level'이 가장 높은 기사 선택
        max_article = max(articles, key=lambda x: int(x['press_level']))
        max_press_articles.append(max_article)

    df = pd.DataFrame(max_press_articles)
    df['count'] = df['cluster_id'].map(cluster_counts)
    df_sorted = df.sort_values(by=['press_level','count'], ascending=[False, False])
    # df_sorted.to_excel(os.path.join(EXCEL_FOLDER, f"{RESULT_ARTICLE}.xlsx"), index=False)

    insertResultHis_WithDf_Keyword(df_sorted, keyword, conn)

    return df_sorted
