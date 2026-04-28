#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# 读取现有的init.json
with open('init.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"原始数据项数: {len(data)}")

# 找到pk=51的索引位置
pk51_index = -1
for i, item in enumerate(data):
    if item.get('model') == 'system.permissions' and item.get('pk') == 51:
        pk51_index = i
        break

print(f"pk=51的索引位置: {pk51_index}")

# 新权限数据
current_time = "2021-03-06T07:36:04.613Z"

# 要插入的新权限列表（pk 52-66）
new_permissions = [
    # 菜单权限 52-54
    {"model": "system.permissions", "pk": 52, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备", "sign": "cmdb-network-devices", "menu": True, "method": "", "path": "", "pid": 44, "desc": ""}},
    {"model": "system.permissions", "pk": 53, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备", "sign": "cmdb-storage-devices", "menu": True, "method": "", "path": "", "pid": 44, "desc": ""}},
    {"model": "system.permissions", "pk": 54, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备", "sign": "cmdb-security-devices", "menu": True, "method": "", "path": "", "pid": 44, "desc": ""}},
    # 网络设备操作权限 55-58
    {"model": "system.permissions", "pk": 55, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备新增", "sign": "cmdb-network-devices-add", "menu": False, "method": "POST", "path": "/cmdb/network-devices/", "pid": 52, "desc": ""}},
    {"model": "system.permissions", "pk": 56, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备删除", "sign": "cmdb-network-devices-del", "menu": False, "method": "DELETE", "path": "/cmdb/network-devices/\\d+/", "pid": 52, "desc": ""}},
    {"model": "system.permissions", "pk": 57, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备批量删除", "sign": "cmdb-network-devices-mdel", "menu": False, "method": "DELETE", "path": "/cmdb/network-devices/", "pid": 52, "desc": ""}},
    {"model": "system.permissions", "pk": 58, "fields": {"create_time": current_time, "update_time": current_time, "name": "网络设备编辑", "sign": "cmdb-network-devices-update", "menu": False, "method": "PUT", "path": "/cmdb/network-devices/\\d+/", "pid": 52, "desc": ""}},
    # 存储设备操作权限 59-62
    {"model": "system.permissions", "pk": 59, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备新增", "sign": "cmdb-storage-devices-add", "menu": False, "method": "POST", "path": "/cmdb/storage-devices/", "pid": 53, "desc": ""}},
    {"model": "system.permissions", "pk": 60, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备删除", "sign": "cmdb-storage-devices-del", "menu": False, "method": "DELETE", "path": "/cmdb/storage-devices/\\d+/", "pid": 53, "desc": ""}},
    {"model": "system.permissions", "pk": 61, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备批量删除", "sign": "cmdb-storage-devices-mdel", "menu": False, "method": "DELETE", "path": "/cmdb/storage-devices/", "pid": 53, "desc": ""}},
    {"model": "system.permissions", "pk": 62, "fields": {"create_time": current_time, "update_time": current_time, "name": "存储设备编辑", "sign": "cmdb-storage-devices-update", "menu": False, "method": "PUT", "path": "/cmdb/storage-devices/\\d+/", "pid": 53, "desc": ""}},
    # 安全设备操作权限 63-66
    {"model": "system.permissions", "pk": 63, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备新增", "sign": "cmdb-security-devices-add", "menu": False, "method": "POST", "path": "/cmdb/security-devices/", "pid": 54, "desc": ""}},
    {"model": "system.permissions", "pk": 64, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备删除", "sign": "cmdb-security-devices-del", "menu": False, "method": "DELETE", "path": "/cmdb/security-devices/\\d+/", "pid": 54, "desc": ""}},
    {"model": "system.permissions", "pk": 65, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备批量删除", "sign": "cmdb-security-devices-mdel", "menu": False, "method": "DELETE", "path": "/cmdb/security-devices/", "pid": 54, "desc": ""}},
    {"model": "system.permissions", "pk": 66, "fields": {"create_time": current_time, "update_time": current_time, "name": "安全设备编辑", "sign": "cmdb-security-devices-update", "menu": False, "method": "PUT", "path": "/cmdb/security-devices/\\d+/", "pid": 54, "desc": ""}},
]

# 在pk=51之后插入新权限
if pk51_index >= 0:
    insert_position = pk51_index + 1
    # 倒序插入，保持顺序
    for perm in reversed(new_permissions):
        data.insert(insert_position, perm)
    
    print(f"已插入 {len(new_permissions)} 个新权限")
else:
    print("错误: 未找到pk=51的权限")

# 更新visitor角色（pk=2）的permissions列表，添加菜单权限52,53,54
for item in data:
    if item.get('model') == 'system.roles' and item.get('pk') == 2:
        original_perms = item['fields']['permissions']
        print(f"visitor原始权限: {original_perms}")
        # 添加新的菜单权限
        for p in [52, 53, 54]:
            if p not in original_perms:
                original_perms.append(p)
        print(f"visitor更新后权限: {original_perms}")
        break

# 保存到文件
with open('init.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

print(f"更新后数据项数: {len(data)}")
print("init.json 已更新完成!")

# 验证更新
with open('init.json', 'r', encoding='utf-8') as f:
    check_data = json.load(f)

# 检查pk 52-66是否存在
print("\n验证新增权限:")
for pk in range(52, 67):
    found = False
    for item in check_data:
        if item.get('model') == 'system.permissions' and item.get('pk') == pk:
            found = True
            print(f"  pk={pk}: {item['fields']['name']} - 已找到 ✓")
            break
    if not found:
        print(f"  pk={pk}: 未找到 ✗")
