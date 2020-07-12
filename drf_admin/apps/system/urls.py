""" 
@author: Wang Meng
@github: https://github.com/tianpangji 
@software: PyCharm 
@file: urls.py 
@create: 2020/6/21 22:24 
"""
from django.urls import path, re_path

from system.views import users

urlpatterns = [
    path(r'users/', users.UsersViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'multiple_delete'})),
    re_path(r'^users/(?P<pk>\d+)$', users.UsersViewSet.as_view({'delete': 'destroy', 'put': 'update'}))
]
