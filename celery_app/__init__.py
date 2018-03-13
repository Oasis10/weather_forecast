# -*- coding: utf-8 -*-

from __future__ import absolute_import
from celery import Celery

app = Celery('weather_forecast')  # 创建 Celery 实例
app.config_from_object('celery_app.celeryconfig')  # 通过 Celery 实例加载配置模块
