# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : backup.py
@create   : 2020/12/9 20:27
"""
import os
import time

from django.conf import settings


def mysql():
    """mysql数据库备份"""
    db_user = ''
    db_pwd = ''
    db_name = ''
    backup_dir = os.path.join(settings.BASE_DIR, 'backup', 'mysql')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    time_strf = time.strftime('%Y-%m-%d_%H-%M-%S')
    sql_file_path = os.path.join(backup_dir, time_strf + '.sql')
    sql_cmd = f'mysqldump --single -transaction -u{db_user} -p{db_pwd} {db_name} > {sql_file_path}'
    os.system(sql_cmd)
