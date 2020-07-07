""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : permissions.py 
@create   : 2020/6/28 21:52 
"""
import re
from collections import defaultdict
from django.conf import settings
from rest_framework.permissions import BasePermission


class RbacPermission(BasePermission):
    """
    自定义权限认证
    """

    def get_user_permissions(self, request):
        if request.user:
            try:
                perms_dict = defaultdict(set)
                perms = request.user.roles.values(
                    'permissions__path',
                    'permissions__method',
                ).distinct()
                for item in perms:
                    # 获取当前用户的权限，并转换为GET/POST/PUT等
                    method = item['permissions__method'].split('_')[-1]
                    if method == 'ALL':
                        perms_dict[item['permissions__path']].add('GET')
                        perms_dict[item['permissions__path']].add('POST')
                        perms_dict[item['permissions__path']].add('PUT')
                        perms_dict[item['permissions__path']].add('DELETE')
                    else:
                        perms_dict[item['permissions__path']].add(method)
                return perms_dict
            except AttributeError:
                return None
        return None

    def has_permission(self, request, view):
        request_url = request.path
        # 如果请求url在白名单，放行
        for safe_url in settings.WHITE_LIST:
            if re.match(settings.REGEX_URL.format(url=safe_url), request_url):
                return True
        method = request.method
        request_perms = self.get_user_permissions(request)
        if request_perms:
            request_url = request._request.path_info.split('/')[2]  # 截取request的路径
            SAFEMETHOD = ('HEAD', 'OPTIONS')
            # 管理员有所有权限
            if 'ADMIN' in request_perms[None]:
                return True
            elif request._request.method in request_perms[request_url]:
                return True
            elif request._request.method in SAFEMETHOD:
                return True
