""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : utils.py 
@create   : 2020/7/11 14:11 
"""
import re

from django.contrib.auth.backends import ModelBackend

from oauth.models import Users


class UsernameMobileAuthBackend(ModelBackend):
    """"重写Django原有的验证方法"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 增加手机号登录
        try:
            if re.match(r'^1[3-9]\d{9}$', username):
                # 判断是手机号
                user = Users.objects.get(mobile=username)
            else:
                user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            user = None

        # 校验密码
        if user is not None and user.check_password(password):
            return user
