@ECHO OFF
celery -A celery_app worker -l info -n app -P eventlet