import pandas as pd
import os
from searchEveryday.searchEveryday.config import EXCEL_FOLDER, RESULT_ARTICLE


def extract_max_press_level_article(cluster_data):
    max_press_articles = []
    cluster_counts = {}
    for cluster, articles in cluster_data.items():
        cluster_counts[cluster] = len(articles)
        # 각 군집의 기사 중 'press_level'이 가장 높은 기사 선택
        max_article = max(articles, key=lambda x: int(x['press_level']))
        max_press_articles.append(max_article)

    df = pd.DataFrame(max_press_articles)
    df['count'] = df['cluster_id'].map(cluster_counts)
    df_sorted = df.sort_values(by=['count', 'press_level'], ascending=[False, False])
    df_sorted.to_excel(os.path.join(EXCEL_FOLDER, f"{RESULT_ARTICLE}.xlsx"), index=False)

    return df_sorted
