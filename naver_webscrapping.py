import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import time

def get_day_list(item_code, page_no):
    """
    일자별 시세를 페이지별로 수집
    """ 
    url = f"https://finance.naver.com/item/news_news.nhn?code={item_code}&page={page_no}&sm=title_entity_id.basic&clusterId="
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html = bs(response.text, "lxml")
    temp = html.select("table")
    table = pd.read_html(str(temp))
    df_temp = table[0]
    return df_temp
    
    
  item_code='051910'
page_no = 1
start_page = 1
end_page = 300

item_list = []
for page_no in range(start_page, end_page + 1):
    df_temp_news = get_day_list(item_code, page_no)
    item_list.append(df_temp_news)
    random_sleep = np.random.uniform(0,1)
    time.sleep(random_sleep)

df = pd.concat(item_list)
