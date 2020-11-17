# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : users.py
@create   : 2020/9/15 21:59
"""
import django_filters

from drf_admin.common.departments import get_departments_id
from oauth.models import Users
from system.models import Departments


class UsersFilter(django_filters.rest_framework.FilterSet):
    """自定义用户管理过滤器"""
    department_id = django_filters.rest_framework.NumberFilter(method='department_service_filter')

    class Meta:
        model = Users
        fields = ['is_active', 'department_id']

    def department_service_filter(self, queryset, name, value):
        """过滤该部门及所有子部门下的用户"""
        return queryset.filter(department_id__in=get_departments_id(value))

    def department_id_filter(self, department_id, department_ids_set):
        departments = Departments.objects.filter(pid=department_id)
        for department in departments:
            department_ids_set.add(department.id)
            self.department_id_filter(department, department_ids_set)
        return department_ids_set
