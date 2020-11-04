# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : config.py
@create   : 2020/8/10 19:20
@docs     : https://docs.celeryproject.org/en/stable/userguide/configuration.html
"""

broker_url = 'redis://127.0.0.1:6379/15'  # 消息中间件配置
# result_backend = 'redis://127.0.0.1:6379/16'  # 默认不开启,后端用于存储任务结果（逻辑删除）
