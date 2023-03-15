# @Time    : 2023/3/12 23:12
# @Author  : tamya2020
# @File    : crawl_list_detail.py
# @Description :
import random

import requests
from celery_app import app
from scrapy.selector import Selector
from urllib.parse import urljoin

from parse_content.get_movie_infos import KnnMaoYanTop100
from parse_content.ohRequest import LoadUserAgent

UAS = LoadUserAgent()
UBS = KnnMaoYanTop100()


# ignore_result=True,忽略结果
@app.task(ignore_result=True)
def crawl_movie_list(url):
    headers = {
        'User-Agent': random.choice(UAS),
    }
    html = requests.get(url, headers=headers).text
    response = Selector(text=html)
    detail_urls = response.xpath("//dl[@class='board-wrapper']/dd/a/@href").extract()
    print(f"list:{len(detail_urls)}")
    for url in detail_urls[0:2]:
        crawl_movie_detail.delay(url)


@app.task
def crawl_movie_detail(url):
    index_url = "https://www.maoyan.com/"
    refer_url = urljoin(index_url, url)
    full_url = urljoin(index_url, "ajax" + url)
    text = UBS.replace_font_text(full_url, refer_url)
    response = Selector(text=text)
    item = dict()
    item["name"] = response.xpath("//*[@class='name']/text()").extract_first().strip()
    item["score"] = response.xpath("//span[@class='index-left info-num ']/span/text()").extract_first()
    box_office = response.xpath("//div[@class='movie-index-content box']/span[1]/text()").extract_first()
    unit = response.xpath("//div[@class='movie-index-content box']/span[2]/text()").extract_first("")
    item["box_office"] = box_office + unit
    print(item)
    return item
