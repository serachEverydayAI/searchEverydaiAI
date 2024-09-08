from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_samples, silhouette_score
import pandas as pd

korean_stop_words = ['의', '가', '이', '은', '는', '을', '를', '에', '와', '과', '도', '로', '에서', '하지만', '또한', '뉴스', '기자', '경우',
                     '기사', '복사', '저작권자', '무단', '송고', '제보', '학습', '활용', '관련', '때문', '최근', '이날', '포트', '오늘', '내일', '영상',
                     '영상편집', '편집', '배포', '금지', '오전', '전재', '재배포', '카카오', '사진', '출처', '가운데', '촬영', '촬영기자', '앵커',
                     '리포트', '관계자', '글쎄', '오늘의', '소식']

MAX_K_VALUE = 100
MIN_CLUSTER_SIZE = 3  # 최소 클러스터 크기 제한


def cluster_articles(df_articles, max_k=MAX_K_VALUE):

    clusters, valid_clusters = [], []
    cluster_silhouette_scores, clustered_articles = {}, {}
    optimal_k = silhouette_avg = None

    if len(df_articles) > 1:
        # 1. 기사 제목을 추출
        titles = df_articles['title'].tolist()

        vectorizer = TfidfVectorizer(stop_words=korean_stop_words)
        X = vectorizer.fit_transform(titles)

        # 2. 최적의 Cluster 수 찾기
        optimal_k, silhouette_avg = find_optimal_clusters(X, max_k=max_k)

        # 3. KMeans 사용해 군집화
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        kmeans.fit(X)

        # 4. 각 기사의 Cluster 할당
        clusters = kmeans.predict(X)
        print_top_words_per_cluster(vectorizer, kmeans)

        # 5. 실루엣 계수를 계산하여 각 클러스터의 평균 계수를 구함
        print(f"Overall Silhouette Score for all clusters: {silhouette_avg}, Cluster Size: {len(set(clusters))}")

    else:
        print(f"Keyword article is one. Nothing to cluseter.")
        clusters.append(0)

    df_articles['cluster_id'] = clusters

    if len(set(clusters)) > 2:
        # 군집수가 2개 이상일 경우, 실루엣 값 계산
        silhouette_vals = silhouette_samples(X, clusters)

        # 6. 클러스터별 평균 실루엣 계수 계산
        for cluster_id in range(optimal_k):
            cluster_silhouette_scores[cluster_id] = silhouette_vals[clusters == cluster_id].mean()

        # 7. 평균 실루엣 계수가 낮은 클러스터를 제외
        valid_clusters = [cluster_id for cluster_id, score in cluster_silhouette_scores.items() if score > silhouette_avg]

        # 8. 유효한 클러스터들만 포함
        filtered_articles = df_articles[df_articles['cluster_id'].isin(valid_clusters)]

        # 9. 클러스터별로 기사들을 저장
        for cluster_id in valid_clusters:
            clustered_articles[cluster_id] = filtered_articles[filtered_articles['cluster_id'] == cluster_id].to_dict(orient='records')
            print_clustered_articles(clustered_articles, cluster_silhouette_scores)
    else:
        df = pd.DataFrame(df_articles)
        clustered_articles = df.groupby('cluster_id').apply(lambda x: x.to_dict(orient='records')).to_dict()

    return clustered_articles


def find_optimal_clusters(X, max_k=MAX_K_VALUE):
    """엘보우 방법과 실루엣 점수를 사용하여 최적의 클러스터 수를 찾습니다."""
    n_samples = X.shape[0]  # 희소 행렬에서 행의 개수를 얻음
    max_k = min(max_k, n_samples - 1)  # max_k가 n_samples보다 크지 않도록 조정
    iters = range(2, max_k + 1)
    sse, silhouette_scores = [], []
    silhouette_avg = None

    for k in iters:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        sse.append(kmeans.inertia_)

        # 실루엣 점수 계산 (클러스터가 샘플 수보다 적을 때만)
        if k < n_samples:
            labels = kmeans.labels_
            silhouette_avg = silhouette_score(X, labels)
            silhouette_scores.append(silhouette_avg)
        else:
            break  # 클러스터 수가 샘플 수보다 많을 때는 중지

    # 엘보우 포인트를 시각화
    # plt.plot(iters, sse, marker='o', label='SSE')
    # plt.plot(iters, silhouette_scores, marker='x', label='Silhouette Score')
    # plt.xlabel('Number of clusters')
    # plt.ylabel('SSE / Silhouette Score')
    # plt.title('Elbow Method and Silhouette Score for Optimal k')
    # plt.legend()
    # plt.show()

    # 실루엣 점수가 가장 높은 클러스터 수 선택
    if silhouette_scores:
        optimal_k = iters[silhouette_scores.index(max(silhouette_scores))]
        print(f"Optimal number of clusters based on silhouette score: {optimal_k}")
    else:
        optimal_k = 2  # 기본값으로 최소 2개의 클러스터 선택
        print("No valid silhouette scores calculated. Defaulting to 2 clusters.")

    return optimal_k, silhouette_avg


def print_clustered_articles(clustered_articles, cluster_silhouette_scores):
    """클러스터 및 실루엣 계수를 출력합니다."""
    # 클러스터 크기 기준으로 정렬
    sorted_clusters = sorted(clustered_articles.items(), key=lambda x: len(x[1]), reverse=True)

    for cluster_id, articles in sorted_clusters:
        print("#" * 80)
        print(f"Cluster {cluster_id} - Number of Articles: {len(articles)}")
        print(f"Silhouette Score: {cluster_silhouette_scores[cluster_id]}")
        print("-" * 80)
        for article in articles:
            print(f"Title: {article['title']}")
            print(f"Press: {article['press']}")
            print(f"Press Level: {article['press_level']}")
            print(f"Link: {article['link']}")
            print("-" * 80)

def print_top_words_per_cluster(vectorizer, kmeans, n_words=10):
    """각 클러스터에서 상위 n개의 중요 단어를 출력"""
    feature_names = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]  # 클러스터 중심의 중요 단어 인덱스 정렬

    for cluster_id in range(kmeans.n_clusters):
        print(f"\nCluster {cluster_id}:")
        top_words = [feature_names[i] for i in order_centroids[cluster_id, :n_words]]
        print(", ".join(top_words))