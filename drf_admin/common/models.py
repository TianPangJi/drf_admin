# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : models.py
@create   : 2020/12/26 18:19
"""


def get_child_ids(pid, models, myself=True, ids: set = None) -> set:
    """
    获取models模型的子id集合
    :param pid: models模型类ID
    :param models: models模型对象
    :param myself: 是否包含pid
    :param ids: 所有ID集合(默认为None)
    :return: ids(所有ID集合)
    """
    if ids is None:
        ids = set()
    queryset = models.objects.filter(pid=pid)
    for instance in queryset:
        ids.add(instance.id)
        get_child_ids(instance.id, models, myself, ids)
    if myself:
        ids.add(pid)
    return ids
