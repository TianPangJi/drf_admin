# 本项目快速开始技巧和指南

## 本项目安装和部署

可以先参考[运行本项目](run_drf.md)文档，文档中有关于运行环境和命令的一些描述。

如果本地使用代理，则可以使用代理安装，可能速度更快，也更自由。

```shell
pip install pysocks5  # 启用pip socks5协议支持
pip install --proxy socks5://127.0.0.1:10808 -r requirements.txt
```

## Pycharm 开发环境准备

> 建议使用专业版的 PyCharm，方便 Django 项目开发

### 解决 PyCharm 提示 import 错误问题

使用Pycharm打开本项目时，将"drf_admin/apps"目录标记为代码根目录（mark as Sources Root），关键词"django import from other app”。

### 启用 Django Console

`Django Console`中的 Environment Variables 需要指定：`DJANGO_SETTINGS_MODULE=drf_admin.settings.dev`

## Django 除错测试 | debug in Django

### 建议使用 pycharm 专业版自带的 Django debug 功能

先创建一个 "Run/Debug Configuration" ，然后即可使用 PyCharm 自带的 debug 功能，方便图形化操作了。

### debug variables of anywhere in django project

参见 issue: https://github.com/TianPangJi/drf_admin/issues/11

```python
import logging

logger = logging.getLogger('django.request')

# do this anywhere
logger.info(" ========> " + " ".join([__name__, str(request), str(kwargs)]))
```

### debug others

[How to debug in Django](https://stackoverflow.com/questions/1118183/how-to-debug-in-django-the-good-way)

[pdb — The Python Debugger](https://docs.python.org/3/library/pdb.html)

```python
import pdb

pdb.set_trace()
```

[pdb 命令语法](https://docs.python.org/3/library/pdb.html#debugger-commands)

## 本项目的一些有用的 URL 路径

### drf

http://localhost:8769/api/oauth/login/

### swagger 链接

http://localhost:8769/api/swagger/

http://localhost:8769/api/redoc/

#### 获取 Authorization Header 内容

在本项目中DRF(Django REST Framework)使用的认证方式是 [JSON Web Token Authentication(JWT)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#usage)
首先使用/oauth/login/接口获取token内容，形如：
```json
{
  "msg": "成功",
  "errors": "",
  "code": 200,
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjE0MDY5NzkxLCJlbWFpbCI6InViZXJ1cmV5X3Vwc0AxNjMuY29tIiwib3JpZ19pYXQiOjE2MTM5ODMzOTF9.r1q4xhItyocOHvzXmd2aQQf6P-ARAtpYzGi6FQsf69g"
  }
}
```
如果将上述响应内容中的"token"的值记作data，则 Authorization 头部内容应该为：`Bearer data`，比如：
```text
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjE0MDY5NzkxLCJlbWFpbCI6InViZXJ1cmV5X3Vwc0AxNjMuY29tIiwib3JpZ19pYXQiOjE2MTM5ODMzOTF9.r1q4xhItyocOHvzXmd2aQQf6P-ARAtpYzGi6FQsf69g
```
然后就可以利用此header请求其他需要认证的接口了。
```shell
curl -X GET "http://127.0.0.1:8769/api/oauth/info/" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjE0MDY5NzkxLCJlbWFpbCI6InViZXJ1cmV5X3Vwc0AxNjMuY29tIiwib3JpZ19pYXQiOjE2MTM5ODMzOTF9.r1q4xhItyocOHvzXmd2aQQf6P-ARAtpYzGi6FQsf69g"
```

除 JWT 之外，DRF 还支持其他第三方认证插件，详情可参考[此链接](https://www.django-rest-framework.org/api-guide/authentication/) 。


## Django 中的自定义验证 | Customizing authentication in Django

https://docs.djangoproject.com/zh-hans/3.1/topics/auth/customizing/

## github 工作流（节选）

先将本项目作为upstream，fork到自己的GitHub账户下，在自己的账户下进行开发。

在需要同步 upstream 时使用如下命令进行操作：

```shell
git remote add upstream https://github.com/TianPangJi/drf_admin.git
git fetch upstream
git merge upstream/master
git push origin master
```

或

```shell
    cd 自己的私有库
    git remote add upstream https://github.com/TianPangJi/drf_admin.git  # 添加公共库到本地
    git remote -v  # 查看本地的remote有哪一些
    git fetch --all  # 从公共库下载所有更改到本地
    git rebase upstream/master  # 将本地私有库与公共库合并，注意rebase只能用于本地库，不能用于远程库
    #git log  # 查看公共库的更改
    git push origin master  # 将公共库上的更改推送到自己的私有库
    # 以上过程都是操作的自己的私有库
```

## 关于静态文件的部署

静态文件，比如图片，JavaScript，CSS、favicon.ico、robots.txt等，建议使用nginx或apache等，而不是依赖Django本身。
可参考 [管理静态文件](https://docs.djangoproject.com/zh-hans/3.1/howto/static-files/) 和 [部署静态文件](https://docs.djangoproject.com/zh-hans/3.1/howto/static-files/deployment/) 。
