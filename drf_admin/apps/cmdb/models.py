from django.db import models

from drf_admin.utils.models import BaseModel, BasePasswordModels


class Assets(BaseModel):
    """所有资产的共有数据表"""

    asset_type_choice = (
        ('server', '服务器'),
        ('network', '网络设备'),
        ('storage', '存储设备'),
        ('security', '安全设备'),
    )

    asset_status_choice = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )

    name = models.CharField(max_length=64, unique=True, verbose_name="资产名称")  # 不可重复
    sn = models.CharField(max_length=128, unique=True, verbose_name="资产序列号")  # 不可重复
    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name="资产类型")
    asset_status = models.SmallIntegerField(choices=asset_status_choice, default=0, verbose_name='设备状态')
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    department = models.ForeignKey('system.Departments', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='所属部门')
    admin = models.ForeignKey('oauth.Users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='资产管理员')
    cabinet = models.ForeignKey('Cabinets', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所在机柜')
    expire_day = models.DateField(null=True, blank=True, verbose_name="过保日期")
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    objects = models.Manager()

    def __str__(self):
        return f'{self.get_asset_type_display()}--{self.name}'

    class Meta:
        db_table = 'cmdb_assets'
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Servers(models.Model):
    """服务器设备"""

    server_system_type_choice = (
        (0, 'Unix'),
        (1, 'Linux'),
        (2, 'Windows'),
        (3, 'Netware'),
    )

    server_type_choice = (
        ('pm', '物理机'),
        ('vm', '虚拟机'),
    )

    asset = models.OneToOneField('Assets', on_delete=models.CASCADE, related_name='server')  # 非常关键的一对一关联
    server_type = models.CharField(max_length=16, choices=server_type_choice, default=0, verbose_name="服务器类型")
    server_system_type = models.SmallIntegerField(choices=server_system_type_choice, default=0, verbose_name="服务器系统类型")
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    use = models.CharField(max_length=128, null=True, blank=True, verbose_name='用途')

    objects = models.Manager()

    def __str__(self):
        return f'{self.get_server_system_type_display()}--{self.get_server_type_display()}--{self.asset.name}'

    class Meta:
        db_table = 'cmdb_servers'
        verbose_name = '服务器'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class SecurityDevices(models.Model):
    """安全设备"""

    device_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (3, '运维审计系统'),
    )

    asset = models.OneToOneField('Assets', on_delete=models.CASCADE, related_name='security')
    device_type = models.SmallIntegerField(choices=device_type_choice, default=0, verbose_name="安全设备类型")
    model = models.CharField(max_length=128, default='未知型号', verbose_name='安全设备型号')

    objects = models.Manager()

    def __str__(self):
        return f'{self.get_device_type_display()}--{self.asset.name}'

    class Meta:
        db_table = 'cmdb_securitydevices'
        verbose_name = '安全设备'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class StorageDevices(models.Model):
    """存储设备"""

    device_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (3, '磁带机'),
    )

    asset = models.OneToOneField('Assets', on_delete=models.CASCADE, related_name='storage')
    device_type = models.SmallIntegerField(choices=device_type_choice, default=0, verbose_name="存储设备类型")
    model = models.CharField(max_length=128, default='未知型号', verbose_name='存储设备型号')

    objects = models.Manager()

    def __str__(self):
        return f'{self.get_device_type_display()}--{self.asset.name}'

    class Meta:
        db_table = 'cmdb_storagedevices'
        verbose_name = '存储设备'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class NetworkDevices(models.Model):
    """网络设备"""

    device_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (3, 'VPN设备'),
    )

    asset = models.OneToOneField('Assets', on_delete=models.CASCADE, related_name='network')
    device_type = models.SmallIntegerField(choices=device_type_choice, default=0, verbose_name="网络设备类型")
    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="VLanIP")
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="内网IP")
    model = models.CharField(max_length=128, default='未知型号', verbose_name="网络设备型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="设备固件版本")
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name="端口个数")
    device_detail = models.TextField(null=True, blank=True, verbose_name="详细配置")

    objects = models.Manager()

    def __str__(self):
        return f'{self.get_device_type_display()}--{self.asset.name}'

    class Meta:
        db_table = 'cmdb_networkdevices'
        verbose_name = '网络设备'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class IDC(BaseModel):
    """机房"""

    name = models.CharField(max_length=64, unique=True, verbose_name="机房名称")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_idc'
        verbose_name = '机房'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Cabinets(BaseModel):
    """机柜"""
    name = models.CharField(max_length=64, unique=True, verbose_name="机柜名称")
    idc = models.ForeignKey('IDC', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="所在机房")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_cabinets'
        verbose_name = '机柜'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Accounts(BasePasswordModels):
    """服务器登录账户表"""
    username = models.CharField(max_length=32, verbose_name='登录账户')
    password = models.CharField(max_length=64, verbose_name='登录密码')
    server = models.ForeignKey('Servers', on_delete=models.CASCADE, verbose_name="服务器", related_name='accounts')
    port = models.PositiveIntegerField(verbose_name='登录端口号')

    objects = models.Manager()

    def __str__(self):
        return f'{self.server.asset.name}--{self.username}'

    class Meta:
        db_table = 'cmdb_accounts'
        verbose_name = '服务器登录账户'
        verbose_name_plural = verbose_name
        ordering = ['id']

# ********************************如下具体资产硬件型号数量,类型等可做自动扫描, 暂不实现*****************************************

# class CPU(models.Model):
#     """CPU组件"""
#
#     asset = models.OneToOneField('Assets', on_delete=models.CASCADE)  # 设备上的cpu肯定都是一样的，所以不需要建立多个cpu数据，一条就可以，因此使用一对一。
#     cpu_model = models.CharField('CPU型号', max_length=128, blank=True, null=True)
#     cpu_count = models.PositiveSmallIntegerField('物理CPU个数', default=1)
#     cpu_core_count = models.PositiveSmallIntegerField('CPU核数', default=1)
#
#     def __str__(self):
#         return self.asset.name + ":   " + self.cpu_model
#
#     class Meta:
#         verbose_name = 'CPU'
#         verbose_name_plural = "CPU"
#
#
# class RAM(models.Model):
#     """内存组件"""
#
#     asset = models.ForeignKey('Assets', on_delete=models.CASCADE)
#     sn = models.CharField('SN号', max_length=128, blank=True, null=True)
#     model = models.CharField('内存型号', max_length=128, blank=True, null=True)
#     manufacturer = models.CharField('内存制造商', max_length=128, blank=True, null=True)
#     slot = models.CharField('插槽', max_length=64)
#     capacity = models.IntegerField('内存大小(GB)', blank=True, null=True)
#
#     def __str__(self):
#         return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)
#
#     class Meta:
#         verbose_name = '内存'
#         verbose_name_plural = "内存"
#         unique_together = ('asset', 'slot')  # 同一资产下的内存，根据插槽的不同，必须唯一
#
#
# class Disk(models.Model):
#     """硬盘设备"""
#
#     disk_interface_type_choice = (
#         ('SATA', 'SATA'),
#         ('SAS', 'SAS'),
#         ('SCSI', 'SCSI'),
#         ('SSD', 'SSD'),
#         ('unknown', 'unknown'),
#     )
#
#     asset = models.ForeignKey('Assets', on_delete=models.CASCADE)
#     sn = models.CharField('硬盘SN号', max_length=128)
#     slot = models.CharField('所在插槽位', max_length=64, blank=True, null=True)
#     model = models.CharField('磁盘型号', max_length=128, blank=True, null=True)
#     manufacturer = models.CharField('磁盘制造商', max_length=128, blank=True, null=True)
#     capacity = models.FloatField('磁盘容量(GB)', blank=True, null=True)
#     interface_type = models.CharField('接口类型', max_length=16, choices=disk_interface_type_choice, default='unknown')
#
#     def __str__(self):
#         return '%s:  %s:  %s:  %sGB' % (self.asset.name, self.model, self.slot, self.capacity)
#
#     class Meta:
#         verbose_name = '硬盘'
#         verbose_name_plural = "硬盘"
#         unique_together = ('asset', 'sn')
#
#
# class NIC(models.Model):
#     """网卡组件"""
#
#     asset = models.ForeignKey('Assets', on_delete=models.CASCADE)  # 注意要用外键
#     name = models.CharField('网卡名称', max_length=64, blank=True, null=True)
#     model = models.CharField('网卡型号', max_length=128)
#     mac = models.CharField('MAC地址', max_length=64)  # 虚拟机有可能会出现同样的mac地址
#     ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
#     net_mask = models.CharField('掩码', max_length=64, blank=True, null=True)
#     bonding = models.CharField('绑定地址', max_length=64, blank=True, null=True)
#
#     def __str__(self):
#         return '%s:  %s:  %s' % (self.asset.name, self.model, self.mac)
#
#     class Meta:
#         verbose_name = '网卡'
#         verbose_name_plural = "网卡"
#         unique_together = ('asset', 'model', 'mac')  # 资产、型号和mac必须联合唯一。防止虚拟机中的特殊情况发生错误。
