# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : ip.py
@create   : 2020/10/3 19:05
"""
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView


class IpBlackListAPIView(ListAPIView, CreateAPIView, DestroyAPIView):
    """

    """
