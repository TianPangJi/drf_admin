from django.contrib import admin

from cmdb.models import Assets, Servers, SecurityDevices, StorageDevices, NetworkDevices, IDC, Cabinets, Accounts

# Register your models here.
admin.site.register(Assets)
admin.site.register(Servers)
admin.site.register(SecurityDevices)
admin.site.register(StorageDevices)
admin.site.register(NetworkDevices)
admin.site.register(IDC)
admin.site.register(Cabinets)
admin.site.register(Accounts)
