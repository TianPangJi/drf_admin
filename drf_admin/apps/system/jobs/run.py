# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : run.py
@create   : 2020/11/28 16:02
"""
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

# django-apscheduler定时任务入口
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)  # BlockingScheduler为阻塞执行, BackgroundScheduler线程异步执行
scheduler.add_jobstore(DjangoJobStore(), 'default')
scheduler.start()
