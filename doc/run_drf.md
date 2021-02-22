# DRF-ADMIN 后台管理系统

#### 后端运行

* 开发使用版本
    * Python 3.6.2(建议使用Python3.x以上版本)
    * Redis 3.2.100
    * MySQL 待使用
* 前置条件
    * 确保已本地已安装Python
    * 确保本地已安装Redis
    * 由于项目使用Windows开发, 暂未在Linux中运行, 建议使用Windows运行(后续将完善)
    * 拉取后端代码**def_admin**
    * 数据库默认使用SQLite, 开发阶段, 后续可能切换为MySQL
    * pip install -r requirements.txt
    * 配置settings/dev.py配置文件修改数据库信息
* 数据库迁移
    * 数据库默认使用SQLite, 开发阶段, 后续可能切换为MySQL
    * 迁移: python manage.py migrate
* 创建登录账户
    * python manage.py createsuperuser
* 启动
    * python manage.py runserver 127.0.0.1:8769
    * python manage.py runserver 0.0.0.0:8769
    * 如修改端口则前端代码也需修改
* 接口文档
    * http://ip:port/api/swagger/

#### 前端运行

* 前置条件
    * 拉取前端代码**fe_admin**
    * 确保本地已安装node.js
    * npm i
* 启动
    * npm run dev