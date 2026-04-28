#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime

# 读取现有的init.json
with open('init.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 找到最后一个权限的pk
last_pk = 0
for item in data:
    if item['model'] == 'system.permissions':
        if item['pk'] > last_pk:
            last_pk = item['pk']

print(f"Last permission pk: {last_pk}")

# 当前时间
current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

# 新权限数据
new_permissions = [
    # 网络设备菜单
    {
        "model": "system.permissions",
        "pk": last_pk + 1,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "网络设备",
            "sign": "cmdb-network-devices",
            "menu": True,
            "method": "",
            "path": "",
            "pid": 44,  # 资产管理
            "desc": ""
        }
    },
    # 存储设备菜单
    {
        "model": "system.permissions",
        "pk": last_pk + 2,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "存储设备",
            "sign": "cmdb-storage-devices",
            "menu": True,
            "method": "",
            "path": "",
            "pid": 44,  # 资产管理
            "desc": ""
        }
    },
    # 安全设备菜单
    {
        "model": "system.permissions",
        "pk": last_pk + 3,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "安全设备",
            "sign": "cmdb-security-devices",
            "menu": True,
            "method": "",
            "path": "",
            "pid": 44,  # 资产管理
            "desc": ""
        }
    },
    # 网络设备操作权限
    {
        "model": "system.permissions",
        "pk": last_pk + 4,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "网络设备新增",
            "sign": "cmdb-network-devices-add",
            "menu": False,
            "method": "POST",
            "path": "/cmdb/network-devices/",
            "pid": last_pk + 1,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 5,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "网络设备删除",
            "sign": "cmdb-network-devices-del",
            "menu": False,
            "method": "DELETE",
            "path": "/cmdb/network-devices/\\d+/",
            "pid": last_pk + 1,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 6,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "网络设备批量删除",
            "sign": "cmdb-network-devices-mdel",
            "menu": False,
            "method": "DELETE",
            "path": "/cmdb/network-devices/",
            "pid": last_pk + 1,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 7,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "网络设备编辑",
            "sign": "cmdb-network-devices-update",
            "menu": False,
            "method": "PUT",
            "path": "/cmdb/network-devices/\\d+/",
            "pid": last_pk + 1,
            "desc": ""
        }
    },
    # 存储设备操作权限
    {
        "model": "system.permissions",
        "pk": last_pk + 8,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "存储设备新增",
            "sign": "cmdb-storage-devices-add",
            "menu": False,
            "method": "POST",
            "path": "/cmdb/storage-devices/",
            "pid": last_pk + 2,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 9,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "存储设备删除",
            "sign": "cmdb-storage-devices-del",
            "menu": False,
            "method": "DELETE",
            "path": "/cmdb/storage-devices/\\d+/",
            "pid": last_pk + 2,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 10,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "存储设备批量删除",
            "sign": "cmdb-storage-devices-mdel",
            "menu": False,
            "method": "DELETE",
            "path": "/cmdb/storage-devices/",
            "pid": last_pk + 2,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 11,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "存储设备编辑",
            "sign": "cmdb-storage-devices-update",
            "menu": False,
            "method": "PUT",
            "path": "/cmdb/storage-devices/\\d+/",
            "pid": last_pk + 2,
            "desc": ""
        }
    },
    # 安全设备操作权限
    {
        "model": "system.permissions",
        "pk": last_pk + 12,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "安全设备新增",
            "sign": "cmdb-security-devices-add",
            "menu": False,
            "method": "POST",
            "path": "/cmdb/security-devices/",
            "pid": last_pk + 3,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 13,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "安全设备删除",
            "sign": "cmdb-security-devices-del",
            "menu": False,
            "method": "DELETE",
            "path": "/cmdb/security-devices/\\d+/",
            "pid": last_pk + 3,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 14,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "安全设备批量删除",
            "sign": "cmdb-security-devices-mdel",
            "menu": False,
            "method": "DELETE",
            "path": "/cmdb/security-devices/",
            "pid": last_pk + 3,
            "desc": ""
        }
    },
    {
        "model": "system.permissions",
        "pk": last_pk + 15,
        "fields": {
            "create_time": current_time,
            "update_time": current_time,
            "name": "安全设备编辑",
            "sign": "cmdb-security-devices-update",
            "menu": False,
            "method": "PUT",
            "path": "/cmdb/security-devices/\\d+/",
            "pid": last_pk + 3,
            "desc": ""
        }
    }
]

# 找到所有权限的位置（在roles之前插入）
roles_index = None
for i, item in enumerate(data):
    if item['model'] == 'system.roles':
        roles_index = i
        break

# 插入新权限
if roles_index is not None:
    for i, perm in enumerate(new_permissions):
        data.insert(roles_index + i, perm)
else:
    # 如果没找到roles，追加到末尾
    data.extend(new_permissions)

# 更新visitor角色的权限（添加新的菜单权限）
for item in data:
    if item['model'] == 'system.roles' and item['pk'] == 2:  # visitor角色
        # 添加新的菜单权限
        item['fields']['permissions'].extend([
            last_pk + 1,  # 网络设备菜单
            last_pk + 2,  # 存储设备菜单
            last_pk + 3,  # 安全设备菜单
        ])

# 保存到文件
with open('init.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("init.json has been updated successfully!")
print(f"Added {len(new_permissions)} new permissions.")
