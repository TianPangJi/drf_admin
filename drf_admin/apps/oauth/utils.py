""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : utils.py 
@create   : 2020/7/11 14:11 
"""
import json
import re

import requests
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


def get_request_ip(request):
    """
    获取请求用户IP
    :param request: request请求对象
    :return: ip
    """
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


def get_ip_address(ip):
    """
    获取IP所在地理位置 (耗时操作暂未使用, 后续可能考虑celery)
    :param ip: ip地址
    :return: address位置信息
    """
    res = requests.request('get', f'http://ip-api.com/json/{ip}')
    if res.status_code == 200:
        dict_data = json.loads(res.text)
        country = dict_data.get('country')
        region_name = dict_data.get('regionName')
        city = dict_data.get('city')
        address = country + ' ' + region_name + ' ' + city
    else:
        address = '未知'
    return address


def get_request_browser(request):
    """
    获取请求用户浏览器信息
    :param request: request请求对象
    :return: 浏览器信息
    """
    family = request.user_agent.browser.family
    version_string = request.user_agent.browser.version_string
    return family + ' ' + version_string


def get_request_os(request):
    """
    获取请求用户系统信息
    :param request: request请求对象
    :return: 系统信息
    """
    family = request.user_agent.os.family
    version_string = request.user_agent.os.version_string
    return family + ' ' + version_string
