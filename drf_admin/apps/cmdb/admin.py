from django.contrib import admin

from cmdb.models import Assets, Servers, SecurityDevices, StorageDevices, NetworkDevices, IDC, Cabinets, Accounts


class ServersInline(admin.StackedInline):
    model = Servers
    verbose_name = '服务器信息'
    verbose_name_plural = '服务器信息'
    can_delete = False


class NetworkDevicesInline(admin.StackedInline):
    model = NetworkDevices
    verbose_name = '网络设备信息'
    verbose_name_plural = '网络设备信息'
    can_delete = False


class StorageDevicesInline(admin.StackedInline):
    model = StorageDevices
    verbose_name = '存储设备信息'
    verbose_name_plural = '存储设备信息'
    can_delete = False


class SecurityDevicesInline(admin.StackedInline):
    model = SecurityDevices
    verbose_name = '安全设备信息'
    verbose_name_plural = '安全设备信息'
    can_delete = False


@admin.register(Assets)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sn', 'asset_type', 'asset_status', 'manage_ip', 'department', 'admin')
    list_filter = ('asset_type', 'asset_status', 'department')
    search_fields = ('name', 'sn', 'manage_ip')
    ordering = ('-id',)
    inlines = [ServersInline, NetworkDevicesInline, StorageDevicesInline, SecurityDevicesInline]


@admin.register(Servers)
class ServersAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset', 'server_type', 'server_system_type', 'model', 'use')
    list_filter = ('server_type', 'server_system_type')
    search_fields = ('asset__name', 'asset__sn', 'model')
    ordering = ('-id',)


@admin.register(NetworkDevices)
class NetworkDevicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset', 'device_type', 'vlan_ip', 'intranet_ip', 'model', 'port_num')
    list_filter = ('device_type',)
    search_fields = ('asset__name', 'asset__sn', 'model', 'vlan_ip', 'intranet_ip')
    ordering = ('-id',)


@admin.register(StorageDevices)
class StorageDevicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset', 'device_type', 'model')
    list_filter = ('device_type',)
    search_fields = ('asset__name', 'asset__sn', 'model')
    ordering = ('-id',)


@admin.register(SecurityDevices)
class SecurityDevicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset', 'device_type', 'model')
    list_filter = ('device_type',)
    search_fields = ('asset__name', 'asset__sn', 'model')
    ordering = ('-id',)


@admin.register(IDC)
class IDCAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'memo', 'create_time')
    search_fields = ('name',)
    ordering = ('-id',)


@admin.register(Cabinets)
class CabinetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'idc', 'memo', 'create_time')
    list_filter = ('idc',)
    search_fields = ('name',)
    ordering = ('-id',)


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'server', 'username', 'port')
    list_filter = ('server__server_type',)
    search_fields = ('server__asset__name', 'username')
    ordering = ('id',)
