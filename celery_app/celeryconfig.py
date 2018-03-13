# -*- coding:utf-8 -*-
from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab

broker_url = 'redis://127.0.0.1:6379'
result_backend = 'redis://127.0.0.1:6379/0'

timezone = 'Asia/Shanghai'

imports = (
    'celery_app.send_mail',
)

# schedule
beat_schedule = {
    # 'add-every-30-seconds': {
    #      'task': 'celery_app.send_mail.send',
    #      'schedule': timedelta(minutes=30),       # 每30分钟执行一次
    #      # 'args': ()
    # },
    'multiply-at-some-time': {
        'task': 'celery_app.send_mail.send',
        'schedule': crontab(minute=0, hour="7, 12, 18"),  # 每天7/12/18点各执行一次
        # 'args': ()
    }
}
