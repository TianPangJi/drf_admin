## 项目安装和部署

先决条件

```shell
pip install --proxy socks5://127.0.0.1:10808 -r D:\GitHub\DingGuodong__drf_admin\requirements.txt
```

## Pycharm 开发环境

### 解决提示 import 错误问题

使用Pycharm打开项目时，将"drf_admin/apps"目录标记为代码根目录（mark as Sources Root），关键词“django import from other app”。

### 启用 Django Console

Django Console中的 Environment Variables 需要指定：DJANGO_SETTINGS_MODULE=drf_admin.settings.dev

## github 工作流

```shell
git remote add upstream https://github.com/TianPangJi/drf_admin.git
git fetch upstream
git merge upstream/master
git push origin master
```

## debug in Django

### debug variables of anywhere in django project

issue: https://github.com/TianPangJi/drf_admin/issues/11

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

|command|alias|annotation|notes|
|----|----|----|----|
|step|s||
|jump|j||
|down|d||
|up|u||
|next|n||
|return|r||

### 建议使用 pycharm 专业版自带的 Django debug 功能

先创建一个 "Run/Debug Configuration" ，然后即可使用 PyCharm 自带的 debug 功能，图形化操作了。

## 项目 URL 路径

### drf

http://localhost:8769/api/oauth/login/

### swagger

http://localhost:8769/api/swagger/

## Django 中的自定义验证 | Customizing authentication in Django

https://docs.djangoproject.com/zh-hans/3.1/topics/auth/customizing/

