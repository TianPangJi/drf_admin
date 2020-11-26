# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : swagger_schema.py
@create   : 2020/11/26 21:27
"""
from drf_yasg.inspectors import SwaggerAutoSchema


class OperationIDAutoSchema(SwaggerAutoSchema):
    """覆盖get_operation_id方法, 添加multiple_delete动作"""

    def get_operation_id(self, operation_keys=None):
        operation_id = super().get_operation_id(operation_keys)
        try:
            if self.view.action == 'multiple_delete':
                return operation_id.replace('delete', 'multiple_delete')
        except AttributeError:
            return operation_id
        return operation_id
