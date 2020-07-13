""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : pagination.py 
@create   : 2020/7/13 21:16 
"""
from rest_framework.pagination import PageNumberPagination


class GlobalPagination(PageNumberPagination):
    page_query_param = 'page'  # 前端发送的页数关键字名，默认为page
    page_size = 10  # 每页数目
    page_size_query_param = 'size'  # 前端发送的每页数目关键字名，默认为None
    max_page_size = 1000  # 前端最多能设置的每页数量
