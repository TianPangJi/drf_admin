## 二、drf_admin(权限RBAC)后台管理系统(配置篇) 
drf_admin采用Python、Django、DRF等技术开发，志在用最短的时间、最简洁的代码，实现开箱即用的后台管理系统。

欢迎访问[drf_admin](https://github.com/TianPangJi/drf_admin)；欢迎star，点个☆小星星☆哦。

## 项目地址
drf_admin（后端）：[https://github.com/TianPangJi/drf_admin](https://github.com/TianPangJi/drf_admin)
fe_admin（前端）：[https://github.com/TianPangJi/fe_admin](https://github.com/TianPangJi/fe_admin)

## 系列文章
* [一、drf_admin(权限RBAC)后台管理系统(介绍篇)](https://blog.csdn.net/Mr_w_ang/article/details/111303774)
* [二、drf_admin(权限RBAC)后台管理系统(配置篇)](https://blog.csdn.net/Mr_w_ang/article/details/113483668)
* [三、drf_admin(权限RBAC)后台管理系统(鉴权篇)](https://blog.csdn.net/Mr_w_ang/article/details/113484448)
* [四、drf_admin(权限RBAC)后台管理系统(RBAC权限篇)]() 留坑

## 一、全局异常处理配置
* 自定义全局异常处理[→官方文档](https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling)
* drf_admin/settings/dev.py配置如下
* ```python
  REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'drf_admin.utils.exceptions.exception_handler',
  }
  ```
* exceptions.py配置如下，添加数据库异常处理及redis异常处理，并处理其他所有未知错误，及记录错误日志。
* ```python
    import logging
    import traceback
    
    from django.core.exceptions import PermissionDenied
    from django.http import Http404
    from rest_framework.exceptions import ErrorDetail
    
    from rest_framework.views import set_rollback
    from django.db import DatabaseError
    from redis.exceptions import RedisError
    from rest_framework.response import Response
    from rest_framework import status, exceptions
    
    # 获取在配置文件中定义的logger，用来记录日志
    from monitor.models import ErrorLogs
    from oauth.utils import get_request_ip
    
    logger = logging.getLogger('error')
    
    
    def errors_handler(exc):
        """
        自定义, 错误消息格式处理
        :param exc:
        :return: data: 错误消息
        """
        try:
            if isinstance(exc.detail, list):
                msg = ''.join([str(x) for x in exc.detail])
            elif isinstance(exc.detail, dict):
                def search_error(detail: dict, message: str):
                    for k, v in detail.items():
                        if k == 'non_field_errors':
                            if isinstance(v, list) and isinstance(v[0], ErrorDetail):
                                message += ''.join([str(x) for x in v])
                            else:
                                message += str(v)
                        else:
                            if isinstance(v, list) and isinstance(v[0], ErrorDetail):
                                message += str(k)
                                message += ''.join([str(x) for x in v])
                            elif isinstance(v, list) and isinstance(v[0], dict):
                                for value_dict in v:
                                    message = search_error(value_dict, message)
                    return message
    
                msg = ''
                msg = search_error(exc.detail, msg)
            else:
                msg = exc.detail
            if not msg:
                msg = exc.detail
        except Exception:
            msg = exc.detail
        data = {'detail': msg}
        return data
    
    
    def exception_handler(exc, context):
        """
        自定义异常处理, 捕获或有异常
        :param exc: 异常
        :param context: 抛出异常的上下文
        :return: Response响应对象
        """
        if isinstance(exc, Http404):
            exc = exceptions.NotFound()
        elif isinstance(exc, PermissionDenied):
            exc = exceptions.PermissionDenied()
    
        if isinstance(exc, exceptions.APIException):
            headers = {}
            if getattr(exc, 'auth_header', None):
                headers['WWW-Authenticate'] = exc.auth_header
            if getattr(exc, 'wait', None):
                headers['Retry-After'] = '%d' % exc.wait
            data = errors_handler(exc)
            set_rollback()
            response = Response(data, status=exc.status_code, headers=headers)
        elif isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            view = context['view']
            # 数据库记录异常
            detail = traceback.format_exc()
            write_error_logs(exc, context, detail)
            logger.error('[%s] %s' % (view, detail))
            response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            # 未知错误
            view = context['view']
            # 数据库记录异常
            detail = traceback.format_exc()
            write_error_logs(exc, context, detail)
            logger.error('[%s] %s' % (view, detail))
            response = Response({'detail': '服务端未知错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
    
    
    def write_error_logs(exc, context, detail):
        """
        记录错误日志信息
        :param exc: 异常
        :param context: 抛出异常的上下文
        :param detail: 异常详情
        :return:
        """
        data = {
            'username': context['request'].user.username if context['request'].user.username else 'AnonymousUser',
            'view': context['view'].get_view_name(),
            'desc': exc.__str__(),
            'ip': get_request_ip(context['request']),
            'detail': detail
        }
        ErrorLogs.objects.create(**data)
    ```

## 二、全局分页配置
* 全局分页配置[→官方文档](https://www.django-rest-framework.org/api-guide/pagination/#pagination)
* drf_admin/settings/dev.py配置如下
* ```python
  REST_FRAMEWORK = {
    # 全局分页
    'DEFAULT_PAGINATION_CLASS': 'drf_admin.utils.pagination.GlobalPagination',
  }
  ```
* pagination.py配置如下
*  ```python
    from rest_framework.pagination import PageNumberPagination
    class GlobalPagination(PageNumberPagination):
        page_query_param = 'page'  # 前端发送的页数关键字名，默认为page
        page_size = 10  # 每页数目
        page_size_query_param = 'size'  # 前端发送的每页数目关键字名，默认为None
        max_page_size = 1000  # 前端最多能设置的每页数量
    ```

## 三、全局响应消息体格式化配置
* 前后端分离项目，规范响应消息体格式，如下：
* ```python
  {'msg': msg, 'errors': detail, 'code': code, 'data': data}
  ```
* 格式化采用Django中间件处理：
* drf_admin/settings/dev.py配置如下:
* ```python
  MIDDLEWARE = [
  'drf_admin.utils.middleware.ResponseMiddleware',
  ]
  ```
* middleware.py配置如下:
* ```python
  class ResponseMiddleware(MiddlewareMixin):
    """
    自定义响应数据格式
    """

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_exception(self, request, exception):
        pass

    def process_response(self, request, response):
        if isinstance(response, Response) and response.get('content-type') == 'application/json':
            if response.status_code >= 400:
                msg = '请求失败'
                detail = response.data.get('detail')
                code = 1
                data = {}
            elif response.status_code == 200 or response.status_code == 201:
                msg = '成功'
                detail = ''
                code = 200
                data = response.data
            else:
                return response
            response.data = {'msg': msg, 'errors': detail, 'code': code, 'data': data}
            response.content = response.rendered_content
        return response
  ```

## 四、日志配置
* 参考drf_admin/settings/dev.py 下的LOGGING配置:

## 五、API文档 Swagger配置
* 参考[→官方文档](https://github.com/axnsan12/drf-yasg)
* 其中使用Token登录配置，参考[→drf-yasg issues58](https://github.com/axnsan12/drf-yasg/issues/58)
* drf_admin/settings/dev.py配置如下:
*   ```python
    SWAGGER_SETTINGS = {
        'USE_SESSION_AUTH': False,
        'SECURITY_DEFINITIONS': {
            'api_key': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        },
    }
    ```
