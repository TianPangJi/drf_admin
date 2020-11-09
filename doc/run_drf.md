<h1 style="text-align: center">DRF-ADMIN 后台管理系统</h1>

#### 后端运行
* 前置条件
    1. 确保已本地已安装Python
    2. 确保本地已安装Redis
    3. 由于项目使用Windows开发, 暂未在Linux中运行, 建议使用Windows运行(后续将完善)
    4. 拉取后端代码**def_admin**
    5. 数据库默认使用SQLite, 开发阶段, 后续可能切换为MySQL
    6. pip install -r requirements.txt
    7. 配置settings/dev.py配置文件修改数据库信息
* 数据库迁移
    1. 数据库默认使用SQLite, 开发阶段, 后续可能切换为MySQL
    2. 迁移: python manage.py migrate
* 创建登录账户
    1. python manage.py createsuperuser
* 启动
    1. python manage.py runserver 0.0.0.0:8769
    2. 如修改端口则前端代码也需修改
* 接口文档
    1. http://ip:port/api/swagger/

#### 前端运行
* 前置条件
    1. 拉取前端代码**fe_admin**
    2. 确保本地已安装node.js
    3. npm i
* 启动
    1. npm run dev