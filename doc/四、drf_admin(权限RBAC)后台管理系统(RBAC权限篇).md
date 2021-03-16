## 四、drf_admin(权限RBAC)后台管理系统(RBAC权限篇)
本篇主要介绍基于Django、DRF(Django REST framework)、RBAC，实现基于角色控制的权限管理

drf_admin采用Python、Django、DRF等技术开发，志在用最短的时间、最简洁的代码，实现开箱即用的后台管理系统。

欢迎访问[drf_admin](https://github.com/TianPangJi/drf_admin)；欢迎star，点个☆小星星☆哦。

## 项目地址
* drf_admin（后端）：[https://github.com/TianPangJi/drf_admin](https://github.com/TianPangJi/drf_admin)
* fe_admin（前端）：[https://github.com/TianPangJi/fe_admin](https://github.com/TianPangJi/fe_admin)

## 系列文章
* [一、drf_admin(权限RBAC)后台管理系统(介绍篇)](https://blog.csdn.net/Mr_w_ang/article/details/111303774)
* [二、drf_admin(权限RBAC)后台管理系统(配置篇)](https://blog.csdn.net/Mr_w_ang/article/details/113483668)
* [三、drf_admin(权限RBAC)后台管理系统(鉴权篇)](https://blog.csdn.net/Mr_w_ang/article/details/113484448)
* [四、drf_admin(权限RBAC)后台管理系统(RBAC权限篇)](https://blog.csdn.net/Mr_w_ang/article/details/114898401)

## RBAC概述
RBAC(Role-Based Access Control,基于角色的访问控制)，通过角色绑定权限，然后给用户划分角色，从而实现权限控制。

优点
## 实现过程
* 流程图
<img src="https://img-blog.csdnimg.cn/2021031620183252.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L01yX3dfYW5n,size_16,color_FFFFFF,t_70#pic_center" border="0" />
* 说明
    1. 前端请求登录，成功后端返回Token值，否则后端返回400
    2. 前端请求获取当前用户信息，成功后根据当前用户信息中的权限信息，进行判断路由及按钮权限判断
    3. 前端请求其他接口，后端先验证登录状态（失败则返回401），再验证用户权限（失败则返回403）
    4. 通过验证后请求进入Django视图
    
## 权限
* 权限流程图
<img src="https://img-blog.csdnimg.cn/20210316201844116.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L01yX3dfYW5n,size_16,color_FFFFFF,t_70#pic_center" border="0" />
* 说明
    1. 根据需求，创建不同角色，例如：admin、visitor
    2. 依据角色，给不同的角色分配不同的权限
    3. 根据用户的岗位及职责分配角色，使不同用户具有不同的权限
    4. 用户请求后端接口时，验证用户权限，通过则放行，否则返回403
    5. 操作数据库

## 实现过程
1. 数据库表设计
    1. Users用户表
    2. Roles角色表
    3. Permissions权限表
    4. Users-Roles(用户角色关联表)
    5. Roles-Permissions(角色权限关联表)
    
    示例：
    <img src="https://img-blog.csdnimg.cn/20210316201859290.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L01yX3dfYW5n,size_16,color_FFFFFF,t_70#pic_center" border="0" />
2. DRF权限官方文档
    1. [DRF官方(权限自定义)](https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions)
3. 代码实现
    * 详细代码请参考[drf-admin](https://github.com/TianPangJi/drf_admin)
    1. 表设计
        1. 用户表
        ```python
        class Users(AbstractUser):
            """
            用户
            """
            name = models.CharField(max_length=20, default='', blank=True, verbose_name='真实姓名')
            mobile = models.CharField(max_length=11, unique=True, null=True, blank=True, default=None, verbose_name='手机号码')
            image = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', blank=True, verbose_name='头像')
            roles = models.ManyToManyField('system.Roles', db_table='oauth_users_to_system_roles', blank=True,
                                           verbose_name='角色')
            department = models.ForeignKey('system.Departments', null=True, blank=True, on_delete=models.SET_NULL,
                                           verbose_name='部门')
        
            class Meta:
                db_table = 'oauth_users'
                verbose_name = '用户'
                verbose_name_plural = verbose_name
                ordering = ['id']
        
                def __str__(self):
                    return self.username
        
                def _get_user_permissions(self):
                    # 获取用户权限
                    permissions = list(filter(None, set(self.roles.values_list('permissions__sign', flat=True))))
                    if 'admin' in self.roles.values_list('name', flat=True):
                        permissions.append('admin')
                        return permissions
        
                    def get_user_info(self):
                        # 获取用户信息
                        user_info = {
                            'id': self.pk,
                            'username': self.username,
                            'name': self.name,
                            'avatar': '/media/' + str(self.image),
                            'email': self.email,
                            'permissions': self._get_user_permissions(),
                            'department': self.department.name if self.department else '',
                            'mobile': '' if self.mobile is None else self.mobile
                        }
                        return user_info
        ```
        2. 角色表
        ```python
        class Roles(BaseModel):
            """
            角色
            """
            name = models.CharField(max_length=32, unique=True, verbose_name='角色')
            permissions = models.ManyToManyField('Permissions', db_table='system_roles_to_system_permissions',
                                                 blank=True, verbose_name='权限')
            desc = models.CharField(max_length=50, blank=True, default='', verbose_name='描述')
        
            objects = models.Manager()
        
            def __str__(self):
                return self.name
        
            class Meta:
                db_table = 'system_roles'
                verbose_name = '角色'
                verbose_name_plural = verbose_name
                ordering = ['id']
            ```
            2. 权限表
            ```python
        class Permissions(BaseModel):
            """
                权限
                """
            method_choices = (
                (u'POST', u'增'),
                (u'DELETE', u'删'),
                (u'PUT', u'改'),
                (u'PATCH', u'局部改'),
                (u'GET', u'查')
            )
        
            name = models.CharField(max_length=30, verbose_name='权限名')
            sign = models.CharField(max_length=30, unique=True, verbose_name='权限标识')
            menu = models.BooleanField(verbose_name='是否为菜单')  # True为菜单,False为接口
            method = models.CharField(max_length=8, blank=True, default='', choices=method_choices, verbose_name='方法')
            path = models.CharField(max_length=200, blank=True, default='', verbose_name='请求路径正则')
            pid = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父权限')
            desc = models.CharField(max_length=30, blank=True, default='', verbose_name='权限描述')
        
            objects = models.Manager()
        
            def __str__(self):
                return self.name
        
            class Meta:
                db_table = 'system_permissions'
                verbose_name = '权限'
                verbose_name_plural = verbose_name
                ordering = ['id']
        ```
    2. settings文件配置
        ```python
        # 指定自定义的用户模型
        AUTH_USER_MODEL = 'oauth.Users'
           
        # DRF权限配置
        REST_FRAMEWORK = {
            'DEFAULT_PERMISSION_CLASSES':
            (
                'rest_framework.permissions.IsAuthenticated',  # 登录验证
                'drf_admin.utils.permissions.RbacPermission',  # 自定义权限认证
            ),
        }
        ```
     3. RbacPermission权限验证文件配置
        ```python
        class UserLock(APIException):
            status_code = status.HTTP_400_BAD_REQUEST
            default_detail = '用户已被锁定,请联系管理员'
            default_code = 'not_authenticated'
        
        
        class RbacPermission(BasePermission):
            """
            自定义权限认证
            """
        
            @staticmethod
            def pro_uri(uri):
                base_api = settings.BASE_API
                uri = '/' + base_api + '/' + uri + '/'
                return re.sub('/+', '/', uri)
        
            def has_permission(self, request, view):
                # 验证用户是否被锁定
                if not request.user.is_active:
                    raise UserLock()
                request_url = request.path
                # 如果请求url在白名单，放行
                for safe_url in settings.WHITE_LIST:
                    if re.match(settings.REGEX_URL.format(url=safe_url), request_url):
                        return True
                # admin权限放行
                conn = get_redis_connection('user_info')
                if conn.exists('user_info_%s' % request.user.id):
                    user_permissions = json.loads(conn.hget('user_info_%s' % request.user.id, 'permissions').decode())
                    if 'admin' in user_permissions:
                        return True
                else:
                    user_permissions = []
                    if 'admin' in request.user.roles.values_list('name', flat=True):
                        return True
                # RBAC权限验证
                # Step 1 验证redis中是否存储权限数据
                request_method = request.method
                if not conn.exists('user_permissions_manage'):
                    redis_storage_permissions(conn)
                # Step 2 判断请求路径是否在权限控制中
                url_keys = conn.hkeys('user_permissions_manage')
                for url_key in url_keys:
                    if re.match(settings.REGEX_URL.format(url=self.pro_uri(url_key.decode())), request_url):
                        redis_key = url_key.decode()
                        break
                else:
                    return True
                # Step 3 redis权限验证
                permissions = json.loads(conn.hget('user_permissions_manage', redis_key).decode())
                method_hit = False  # 同一接口配置不同权限验证
                for permission in permissions:
                    if permission.get('method') == request_method:
                        method_hit = True
                        if permission.get('sign') in user_permissions:
                            return True
                else:
                    if method_hit:
                        return False
                    else:
                        return True
        ```
