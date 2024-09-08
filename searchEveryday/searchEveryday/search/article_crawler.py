import requests, random, time
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
from searchEveryday.searchEveryday.common.definition import MAIN_PRESS
from searchEveryday.searchEveryday.config import EXCEL_FOLDER


def crawl_articles(keyword: str, filename: str)  -> pd.DataFrame:
    max_page = 50
    sort = 0  # 관련도순
    photo = 0  # 사진 포함 안함
    field = 0  # 제목 + 본문
    all_articles = []
    unique_links = set()  # 중복된 링크를 추적하기 위한 set
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(max_page):
        try:
            url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort={sort}&photo={photo}&field={field}&pd=4&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1d&is_sug_officeid=0&office_category=0&service_area=0&start={page*10+1}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            time.sleep(random.random() + 1)
            if response.status_code != 200:
                raise Exception(f"Failed to load page {url}")
            news = soup.find_all('div', class_='news_wrap api_ani_send')
            if not news:
                break
            articles = []
            for cnt, item in enumerate(news, start=1):
                title = item.find('a', class_='news_tit').get_text()
                link = item.find('a', class_='news_tit')['href']
                press = item.find('a', class_='info press').get_text()
                current_time = datetime.now()  # 크롤링 시간
                level = MAIN_PRESS.get(press, '0')

                # 중복된 링크인지 확인
                if link not in unique_links:
                    articles.append({
                        'title': title,
                        'content': 'content',
                        'link': link,
                        'press': press,
                        'press_level': level,
                        'crawling_time': current_time
                    })
                    unique_links.add(link)  # 중복 방지를 위해 추가
                    print(f'{page}{cnt - 1} {articles[-1]}')
            all_articles.extend(articles)

        except Exception as e:
            print(e)

    df = pd.DataFrame(all_articles)

    df.to_excel(os.path.join(EXCEL_FOLDER, f"{filename}"), index=False)
    return df
