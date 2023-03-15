# @Time    : 2023/3/11 16:29
# @Author  : tamya2020
# @File    : celery_config.py
# @Description : 
# 官方配置文档：查询每个配置项的含义。
# http://docs.celeryproject.org/en/latest/userguide/configuration.html

import sys
from celery.schedules import crontab
from celery import platforms

sys.path.insert(0, '..')
platforms.C_FORCE_ROOT = True

# broker(消息中间件来接收和发送任务消息)
# broker_url = 'amqp://guest:guest@localhost:5672//'
broker_url = 'redis://localhost:6379/1'
# backend(存储worker执行的结果)
celery_result_backend = 'redis://localhost:6379/2'

# 设置时间参照，不设置默认使用的UTC时间
celery_timezone = 'Asia/Shanghai'
# 设置任务的序列话方式
celery_task_serializer = 'json'
# 设置结果的序列化方式
celery_result_serializer = 'json'
# 每个worker执行了多少任务就会死掉
celeryd_max_tasks_per_child = 40
