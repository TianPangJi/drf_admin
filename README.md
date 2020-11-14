<h1 style="text-align: center">DRF-ADMIN 后台管理系统</h1>

#### 项目简介
一个基于 Django、Django REST framework（DRF）、Channels、Redis、Vue的前后端分离的后台管理系统

项目正在开发中......

#### 项目源码

|     |   后端源码  |   前端源码  |
|---  |--- | --- |
|  github   |  https://github.com/TianPangJi/drf_admin   |  https://github.com/TianPangJi/fe_admin   |

####  系统功能
- 系统管理
    - 用户管理: 提供用户的相关配置及用户筛选，新增用户后，默认密码为123456
    - 角色管理: 对权限进行分配，可依据实际需要设置角色
    - 权限管理: 权限自由控制，增删改查等
    - 部门管理: 可配置系统组织架构，树形表格展示
- 系统监控
    - 在线用户: 在线用户监控
    - IP黑名单: 实现系统IP黑名单拉黑功能
    - 错误日志: 显示后台未知错误及其详情信息
    - 服务监控: 实时监控查看后台服务器性能
- 资产管理
    - 服务器管理: 服务器增删改查
    - 网络设备: ~~待实现~~
    - 存储设备: ~~待实现~~
    - 安全设备: ~~待实现~~
- 工作管理
    - 我的空间: ~~待实现~~
    - 需求管理: ~~待实现~~
- 系统工具
    - 系统接口: 展示后台接口--Swagger
- 个人中心
    - 个人信息管理

#### 系统预览
~~日后完善，留坑~~

#### 启动项目
[点击查看](https://github.com/TianPangJi/drf_admin/blob/master/doc/run_drf.md)

#### 代码结构
<table>
    <tr>
        <td><img src="https://img-blog.csdnimg.cn/2020111416290077.png" border="0" /></td>
        <td><img src="https://img-blog.csdnimg.cn/20201114162859446.png" border="0" /></td>
    </tr>
    <tr>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858969.png" border="0" /></td>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858867.png" border="0" /></td>
    </tr>
    <tr>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858866.png" border="0" /></td>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858950.png" border="0" /></td>
    </tr>
    <tr>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858834.png" border="0" /></td>
        <td><img src="https://img-blog.csdnimg.cn/20201114162859656.png" border="0" /></td>
    </tr>
</table>

#### 特别鸣谢
- 感谢 [JetBrains](https://www.jetbrains.com/) 提供的非商业开源软件开发授权
- 感谢 [Django](https://github.com/django/django) 提供后端Django框架
- 感谢 [DRF](https://github.com/encode/django-rest-framework) 提供后端DRF框架
- 感谢 [PanJiaChen](https://github.com/PanJiaChen/vue-element-admin) 提供的前端模板
- 感谢 [EL-ADMIN](https://github.com/elunez/eladmin) 提供的页面布局及前端模板
