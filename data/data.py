import os
import time  # 💡 导入时间模块，用于翻页减速
import pandas as pd
import requests
import logging
from lxml import etree


def data_get():
    """
    获取数据
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    #总列表
    data_raw = []

    for start in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={start}"
        logging.info(f"开始网络请求: 正在爬取第 {int(start / 25) + 1} 页 -> {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                logging.warning(f"网络请求失败，错误状态码: {response.status_code}")
                continue
        except Exception as e:
            logging.error(f"网络请求发生异常: {e}")
            continue

        """
        解析数据
        """
        html = etree.HTML(response.text)
        movie_items = html.xpath('//ol[@class="grid_view"]/li')

        for movie in movie_items:
            ranking = movie.xpath('.//div[@class="pic"]/em/text()')
            title = movie.xpath('.//div[@class="hd"]/a/span[@class="title"]/text()')
            rating = movie.xpath('.//div[@class="bd"]//span[@class="rating_num"]/text()')
            comment_text = movie.xpath('.//span[contains(text(), "人评价")]/text()')

            ranking_val = ranking[0] if ranking else None
            title_val = title[0] if title else None
            rating_val = rating[0] if rating else None
            comment_val = comment_text[0] if comment_text else None

            data_raw.append({
                "排名": ranking_val,
                "电影名称": title_val,
                "豆瓣评分": rating_val,
                "评价人数": comment_val
            })

        time.sleep(0.5)

    df = pd.DataFrame(data_raw)

    """
    本地存储数据
    """
    os.makedirs("data_list", exist_ok=True)

    raw_csv_path = "data_list/data_raw.csv"
    df.to_csv(raw_csv_path, index=False, encoding="utf-8-sig")
    logging.info(f"数据已保存至：{raw_csv_path}")

    """
    数据清洗
    """
    df_null = df.isnull().sum()

    df.dropna(inplace=True)

    df_null = df.isnull().sum()

    df.drop_duplicates(inplace=True)

    df['评价人数'] = df['评价人数'].str.replace('人评价', '').str.strip()
    logging.info("清洗完毕")

    return df