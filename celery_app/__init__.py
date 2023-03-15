# @Time    : 2023/3/11 16:27
# @Author  : tamya2020
# @File    : __init__.py.py
# @Description : 

from celery import Celery

app = Celery(
    'celery_app',
    include=[
        'celery_app.crawl_list_detail',
    ]
)
app.config_from_object('celery_app.celery_config')
