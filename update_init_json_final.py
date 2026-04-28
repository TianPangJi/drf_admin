#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# 读取现有的init.json
with open('init.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total items in init.json: {len(data)}")

# 找到最后一个权限的pk
last_permission_pk = 0
last_permission_index = -1
for i, item in enumerate(data):
    if item['model'] == 'system.permissions':
        if item['pk'] > last_permission_pk:
            last_permission_pk = item['pk']
            last_permission_index = i

print(f"Last permission pk: {last_permission_pk}")
print(f"Last permission index: {last_permission_index}")
print(f"Last permission: {data[last_permission_index]}")

# 新权限数据
current_time = "2021-03-06T07:36:04.613Z"
new_permissions = [
    {"model": "system.permissions", "pk": 52, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备", "sign": "cmdb-network-devices", "menu": True, "method": "", "path": "", "pid": 44, "desc": ""}},
    {"model": "system.permissions", "pk": 53, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备", "sign": "cmdb-storage-devices", "menu": True, "method": "", "path": "", "pid": 44, "desc": ""}},
    {"model": "system.permissions", "pk": 54, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备", "sign": "cmdb-security-devices", "menu": True, "method": "", "path": "", "pid": 44, "desc": ""}},
    {"model": "system.permissions", "pk": 55, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备新增", "sign": "cmdb-network-devices-add", "menu": False, "method": "POST", "path": "/cmdb/network-devices/", "pid": 52, "desc": ""}},
    {"model": "system.permissions", "pk": 56, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备删除", "sign": "cmdb-network-devices-del", "menu": False, "method": "DELETE", "path": "/cmdb/network-devices/\\d+/", "pid": 52, "desc": ""}},
    {"model": "system.permissions", "pk": 57, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备批量删除", "sign": "cmdb-network-devices-mdel", "menu": False, "method": "DELETE", "path": "/cmdb/network-devices/", "pid": 52, "desc": ""}},
    {"model": "system.permissions", "pk": 58, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备编辑", "sign": "cmdb-network-devices-update", "menu": False, "method": "PUT", "path": "/cmdb/network-devices/\\d+/", "pid": 52, "desc": ""}},
    {"model": "system.permissions", "pk": 59, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备新增", "sign": "cmdb-storage-devices-add", "menu": False, "method": "POST", "path": "/cmdb/storage-devices/", "pid": 53, "desc": ""}},
    {"model": "system.permissions", "pk": 60, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备删除", "sign": "cmdb-storage-devices-del", "menu": False, "method": "DELETE", "path": "/cmdb/storage-devices/\\d+/", "pid": 53, "desc": ""}},
    {"model": "system.permissions", "pk": 61, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备批量删除", "sign": "cmdb-storage-devices-mdel", "menu": False, "method": "DELETE", "path": "/cmdb/storage-devices/", "pid": 53, "desc": ""}},
    {"model": "system.permissions", "pk": 62, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备编辑", "sign": "cmdb-storage-devices-update", "menu": False, "method": "PUT", "path": "/cmdb/storage-devices/\\d+/", "pid": 53, "desc": ""}},
    {"model": "system.permissions", "pk": 63, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备新增", "sign": "cmdb-security-devices-add", "menu": False, "method": "POST", "path": "/cmdb/security-devices/", "pid": 54, "desc": ""}},
    {"model": "system.permissions", "pk": 64, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备删除", "sign": "cmdb-security-devices-del", "menu": False, "method": "DELETE", "path": "/cmdb/security-devices/\\d+/", "pid": 54, "desc": ""}},
    {"model": "system.permissions", "pk": 65, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备批量删除", "sign": "cmdb-security-devices-mdel", "menu": False, "method": "DELETE", "path": "/cmdb/security-devices/", "pid": 54, "desc": ""}},
    {"model": "system.permissions", "pk": 66, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备编辑", "sign": "cmdb-security-devices-update", "menu": False, "method": "PUT", "path": "/cmdb/security-devices/\\d+/", "pid": 54, "desc": ""}},
]

# 插入新权限到最后一个权限之后
insert_index = last_permission_index + 1
for i, perm in enumerate(new_permissions):
    data.insert(insert_index + i, perm)
print(f"Inserted {len(new_permissions)} new permissions at index {insert_index}")

# 更新visitor角色的权限（添加新的菜单权限）
for item in data:
    if item['model'] == 'system.roles' and item['pk'] == 2:  # visitor角色
        print(f"Original visitor permissions: {item['fields']['permissions']}")
        # 添加新的菜单权限（网络设备、存储设备、安全设备菜单）
        item['fields']['permissions'].extend([52, 53, 54])
        print(f"Updated visitor permissions: {item['fields']['permissions']}")

# 保存到文件
with open('init.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

print("init.json has been updated successfully!")
print(f"Total items after update: {len(data)}")
