from django.db import models

from drf_admin.utils.models import BaseModel


# Create your models here.
class Tasks(BaseModel):
    """工作任务"""

    status_choice = (
        (0, '待审核'),
        (1, '待下发'),
        (2, '进行中'),
        (3, '已超时'),
        (4, '待验收'),
        (5, '完成'),
    )

    name = models.CharField(max_length=32, verbose_name='任务名')
    desc = models.TextField(verbose_name='任务详情')
    expire_day = models.DateField(verbose_name="完成时间")
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name='任务状态')
    progress = models.SmallIntegerField(default=0, verbose_name='任务进度')
    creator = models.ForeignKey('oauth.Users', on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    reviewer = models.ForeignKey('oauth.Users', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='审核人')
    executor = models.ForeignKey('oauth.Users', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='执行人')
    department = models.ForeignKey('system.Departments', on_delete=models.SET_NULL, null=True, verbose_name='所属部门')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'work_tasks'
        verbose_name = '工作任务'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']


class TasksProgress(BaseModel):
    """任务进展"""

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    detail = models.TextField(verbose_name='任务进展')
    creator = models.ForeignKey('oauth.Users', on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    task = models.ForeignKey('Tasks', on_delete=models.CASCADE, verbose_name='所属任务')

    class Meta:
        db_table = 'work_tasksprogress'
        verbose_name = '任务进展'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
