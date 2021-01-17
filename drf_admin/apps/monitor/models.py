from django.db import models

from drf_admin.utils.models import BaseModel


# Create your models here.
class ErrorLogs(BaseModel):
    """
    错误日志
    """
    username = models.CharField(max_length=32, verbose_name='用户')
    view = models.CharField(max_length=32, verbose_name='视图')
    desc = models.TextField(verbose_name='描述')
    ip = models.GenericIPAddressField(verbose_name='IP')
    detail = models.TextField(verbose_name='详情')

    objects = models.Manager()

    class Meta:
        db_table = 'monitor_errorlogs'
        verbose_name = '错误日志'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class IpBlackList(BaseModel):
    """
    ip黑名单
    """
    ip = models.GenericIPAddressField(unique=True, verbose_name='IP')

    objects = models.Manager()

    class Meta:
        db_table = 'monitor_ipblacklist'
        verbose_name = 'IP黑名单'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class OnlineUsers(BaseModel):
    """
    在线用户
    """
    user = models.ForeignKey('oauth.Users', on_delete=models.CASCADE, verbose_name='用户')
    ip = models.GenericIPAddressField(verbose_name='IP')

    objects = models.Manager()

    class Meta:
        db_table = 'monitor_onlineusers'
        verbose_name = '在线用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']
