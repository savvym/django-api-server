# Django-Celery-API-Server
## 框架介绍
基于 Nginx、uwsgi、Django、Celery  
Django v5.0.7  
Celery v5.4.0  
### 目录结构
```
.
├── apps
│   ├── cgi
├── etc
├── framework
│   ├── common
│   ├── logging.py
│   ├── static.py
│   ├── context.py
│   ├── router.py
├── project
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile
├── Makefile
├── manage.py
├── requirements.txt
```
- apps 存放业务代码  
- etc 存放一些配置文件
- framework 中是框架中的一些基本工具类
    - static.py 进程的静态存储区：用来提供具有进程级生命周期的变量。
    - context.py 提供一个线程级别 context, 可以提供请求级上下文
    - router.py 提供 cgi 接口类型路由，配合 django 原生路由
    - logging.py 提供的日志 filter， 比如可以打印 request_id
- project 中是 Django 框架的一些基本配置文件  
- manage.py 是 Django 的管理工具，具体用法参考 [django-admin and manage.py](https://docs.djangoproject.com/en/5.0/ref/django-admin/)  

## 使用
### 安装依赖
```
$ pip install -r requirements
```
安装 `mysqlclient` 报错 `Exception: Can not find valid pkg-config name`。 安装 `apt-get install libmysqlclient-dev`.

### 通过 Django 自带 wsgi server 启动
```
$ python manage.py runserver 0.0.0.0:8000
```
### 通过 Nginx + uwsgi 配置启动
```
$ uwsgi --ini etc/uwsgi.ini
```
### 通过 docker 启动
```
# 构建
$ docker build -t app:v1 .
# 启动
$ docker run -itd -p 8080:80 app:v1
```
## 增加新接口
### 添加 Django App  
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
### 添加 cgi 接口
1. 文件加载配置是在 bussiness 中的 `__init__.py` 中的 `mount`方法。
2. 默认是加载 bussiness 下的子文件夹里的所有 python 文件，通过文件名或者 `@schema.request()` 的 `name` 来指定每个文件的路由。
3. 添加新的 cgi 接口： 新建文件夹后添加业务 python 文件
```python
import logging

from pydantic import BaseModel, Field
from framework.router import action, schema
from framework.static import get_current_request_id
from framework import context

logger = logging.getLogger('django')

class AddReqeustModel(BaseModel):
    Action: str = Field(description="An string parameter")
    Args: list = Field(description="A list parameter", default=list())

@action(desc='Add加法接口')
@schema.request(validator = AddReqeustModel)
@schema.response()
def entry(**args):
    logger.info('start add')
    request_id = get_current_request_id()
    ret = {
        'msg': 'this is a add',
    }
    return ret

```
4. 注解说明
- `action` 提供接口路由发现
- `schema.request` 提供请求预处理
- `schema.response` 提供响应处理

## 启动 Celery
### 启动 Worker
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


