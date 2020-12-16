""" 
@author: Wang Meng
@github: https://github.com/tianpangji 
@software: PyCharm 
@file: urls.py 
@create: 2020/6/21 22:24 
"""
from django.urls import path, include

from drf_admin.utils import routers
from system.views import users, roles, permissions, departments, jobs

router = routers.AdminRouter()
router.register(r'users', users.UsersViewSet, basename="users")  # 用户管理
router.register(r'roles', roles.RolesViewSet, basename="roles")  # 角色管理
router.register(r'permissions', permissions.PermissionsViewSet, basename="permissions")  # 权限管理
router.register(r'departments', departments.DepartmentsViewSet, basename="departments")  # 部门管理

urlpatterns = [
    path('users/reset-password/<int:pk>/', users.ResetPasswordAPIView.as_view()),  # 重置密码
    path('users/<int:pk>/permissions/', users.PermissionsAPIView.as_view()),  # 用户权限ID列表
    path('permissions/methods/', permissions.PermissionsMethodsAPIView.as_view()),  # 权限models方法列表信息
    path('jobs/functions/', jobs.JobFunctionsListAPIView.as_view()),  # 调度任务函数
    path('jobs/', jobs.JobsListCreateAPIView.as_view()),  # 调度任务列表,新增,清空
    path('jobs/<uuid:pk>/', jobs.JobUpdateDestroyAPIView.as_view()),  # 调度任务启动/恢复,删除
    path('jobs/executions/', jobs.JobExecutionsListAPIView.as_view()),  # 调度任务执行过程记录
    path('', include(router.urls)),
]
