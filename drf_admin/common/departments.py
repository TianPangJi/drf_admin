# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : departments.py
@create   : 2020/10/24 8:36
"""
from system.models import Departments


def get_departments_id(department_id, departments_id: set = None):
    """
    获取该部门及其所有子部门的id集合
    :param department_id: 部门(Departments)id
    :param departments_id: 默认为None(所有ID集合)
    :return: id集合
    """
    departments = Departments.objects.filter(pid=department_id)
    for department in departments:
        departments_id.add(department.id)
        get_departments_id(department, departments_id)
    departments_id.add(department_id)
    return departments_id
