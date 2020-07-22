""" 
@author: Wang Meng
@github: https://github.com/tianpangji 
@software: PyCharm 
@file: urls.py 
@create: 2020/6/21 22:24 
"""
from django.urls import path, re_path

from system.views import users, roles, permissions as  p

urlpatterns = [
    # 用户管理
    path(r'users/', users.UsersViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'multiple_delete'})),
    re_path(r'^users/(?P<pk>\d+)$',
            users.UsersViewSet.as_view({'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
    # 角色管理
    path(r'roles/', roles.RolesViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'multiple_delete'})),
    re_path(r'^roles/(?P<pk>\d+)$', roles.RolesViewSet.as_view({'delete': 'destroy', 'put': 'update'})),
    # 权限管理
    path(r'permissions/', p.PermissionsViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'multiple_delete'})),
    re_path(r'^permissions/(?P<pk>\d+)$', p.PermissionsViewSet.as_view({'delete': 'destroy', 'put': 'update'})),
]
