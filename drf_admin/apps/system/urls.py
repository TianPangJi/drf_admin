""" 
@author: Wang Meng
@github: https://github.com/tianpangji 
@software: PyCharm 
@file: urls.py 
@create: 2020/6/21 22:24 
"""
from django.urls import path, re_path, include

from drf_admin.utils import routers
from system.views import users, roles, permissions

router = routers.AdminRouter()
router.register(r'users', users.UsersViewSet, basename="users")  # 用户管理
router.register(r'roles', roles.RolesViewSet, basename="roles")  # 角色管理
router.register(r'permissions', permissions.PermissionsViewSet, basename="permissions")  # 权限管理

urlpatterns = [
    path('', include(router.urls)),
]
