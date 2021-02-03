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

## debug variables of anywhere in django project

issue: https://github.com/TianPangJi/drf_admin/issues/11

```python
import logging
logger = logging.getLogger('django.request')

# do this anywhere
logger.info(" ========> " + " ".join([__name__, str(request), str(kwargs)]))
```