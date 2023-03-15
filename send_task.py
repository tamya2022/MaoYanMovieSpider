# @Time    : 2023/3/12 22:03
# @Author  : tamya2020
# @File    : send_task.py
# @Description : 
from celery_app.crawl_list_detail import crawl_movie_list

URL_BASH_1 = "https://www.maoyan.com/board/4?offset={}"

if __name__ == '__main__':
    for i in range(0, 10, 10):
        url = URL_BASH_1.format(i)
        crawl_movie_list.delay(url)
    print("finish!!!")
