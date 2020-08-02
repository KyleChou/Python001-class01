# 学习笔记

## 开发环境配置

Django 最初被设计用于具有快速开发需求的新闻类站点，目的是要实现简单快捷的网站开发。

### MVC 设计模式 

>  设计模式: 前人根据开发经验，沉淀下来的一套编程的指导思想

### MTV 框架模式

* 模型（Model）
* 模版（Template）
* 视图（Views）

![image-20200801180629213](./image-20200801180629213.png)

### Django 的特点

* 采用了 MTV 框架
* 强调快速开发和代码复用 DRY（Do not Repeat Yourself）
* 组件丰富

> ORM （对象关系映射）映射类来构建数据模型
>
> URL 支持正则表达式
>
> 模版可继承
>
> 内置用户认证，提供用户认证和权限功能
>
> admin 管理系统
>
> 内置表单模型、Cache 缓存系统、国际化系统等

Django 学习使用 2.2.13 （LTS 版本）

```shell
pip install --upgrade django==2.2.13

```

## 创建项目和目录结构

启动 Django 分成三个部分

1. 创建 Django 项目
2. 创建应用程序
3. 启动 Django

使用 django-admin 来创建 Django 项目

```shell
# 创建项目 MyDjango
django-admin startproject MyDjango

tree .
.
├── MyDjango
│   ├── __init__.py
│   ├── settings.py # 项目的配置文件
│   ├── urls.py
│   └── wsgi.py
└── manage.py	      # 命令行工具 

python manage.py help # 查看功能

python manage.py startapp index # 启动 index 应用 （主页）

tree index 
index
├── __init__.py
├── admin.py         # 管理后台
├── apps.py          # 当前 app 配置文件
├── migrations       # 数据库迁移文件夹
│   └── __init__.py
├── models.py        # 模型
├── tests.py         # 自动化测试
└── views.py         # 视图

python manage.py runserver # 运行

python manage.py runserver 0.0.0.0:80 # 80 端口启动，允许 lan 访问

```

> 基于安全考虑，测试完成之后需要停止 Django serve、

## 解析 settings.py 主要配置文件

配置文件包括：

* 项目路径
* 密钥
* 域名访问权限
* App 列表
* 静态资源，包括 CSS、JavaScript 图片等
* 模版文件
* 数据库配置
* 缓存
* 中间件

## urls 调度器

MyDjango/urls.py 文件中的 urlpatterns 列表，实现了:

* 从 URL 路由到视图 (views) 的映射功能
* 过程中使用了一个 Python 模块，**URLconf**(URL configuration)，通常这个功能 也被称作 URLconf

### Django 如何处理一个请求

当一个用户请求 Django 站点的一个页面:

1. 如果传入 HttpRequest 对象拥有 urlconf 属性(通过中间件设置)，它的值将被用来代替

   ROOT_URLCONF 设置。

2. Django 加载 URLconf 模块并寻找可用的 urlpatterns，Django 依次匹配每个 URL 模式，在与

   请求的 URL 匹配的第一个模式停下来。

3. 一旦有 URL 匹配成功，Djagno 导入并调用相关的视图，视图会获得如下参数:

>  一个 HttpRequest 实例
>
> 一个或多个位置参数提供

4. 如果没有 URL 被匹配，或者匹配过程中出现了异常，Django 会调用一个适当的错误处理视图。