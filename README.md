# 分布式任务系统 lb_chore_proj
## 框架介绍
基于 Nginx、uwsgi、Django、Celery  
Django v5.0.7  
Celery v5.4.0  
### 目录结构
```
.
├── apps
│   ├── demoapp
├── etc
├── framework
│   ├── utils
│   ├── adapter
│   ├── task
├── project
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static
├── log
├── .env
├── Dockerfile
├── Makefile
├── manage.py
├── requirements.txt
```
- apps 存放业务代码  
- etc 存放一些启动配置文件
- framework 中是框架中的一些基本工具和类，比如统一的错误码和Response结构体等。  
- project 中是框架的一些基本配置文件  
- manage.py 是 Django 的管理工具，具体用法参考 [django-admin and manage.py](https://docs.djangoproject.com/en/5.0/ref/django-admin/)  
- log 文件夹存放日志文件
- .env 存放环境变量
## 使用
### 运行
1.通过 Django 自带 wsgi server 启动
```
$ python manage.py runserver 0.0.0.0:8000
```
2. 通过 Nginx + uwsgi 配置启动
```
```
### 增添新的业务  
1. 在 apps/ 中创建一个文件夹 myapp
2. 使用命令 `django-admin startapp name apps/myapp` 会自动在目录中生成基础代码
3. 在 `apps/myapp` 文件夹下创建 `urls.py` 文件、 celery所需的 `tasks.py` 文件
```
myapp
├── __init__.py
├── admin.py
├── apps.py
├── migrations
├── models.py
├── tests.py
├── tasks.py
├── urls.py
└── views.py
```
4. 修改 `apps.py` 中的类名称和 `name` 属性。
5. 在 `lbcelery/settings.py` 中的 `INSTALLED_APPS` 增加新的 app `apps.myapp.apps.MyAppConfig`。
6. 在 `lbcelery/urls.py` 中的 `urlpatterns` 增加 `path('myapp/', include('myapp.urls'))`。

### 启动 Celery
#### 启动 Worker
1. 直接启动一个 Worker
```
$ celery -A project worker -l INFO
```
2. gevent 协程模式启动
```
$ celery -A project worker -P gevent -c 1000 -l INFO
```
3. 后台启动，使用 `multi` 命令请参考[celery-in-the-background](https://docs.celeryq.dev/en/stable/getting-started/next-steps.html#in-the-background)。更多用法请参考 [multi module](https://docs.celeryq.dev/en/stable/reference/celery.bin.multi.html#module-celery.bin.multi)。

## 接口
// TODO