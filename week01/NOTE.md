学习笔记

## 1. 用requests写一个最简单的爬虫

python 开发项目步骤
1. 提出需求
（我们具体需要完成一个什么样的任务）
2. 编码
（根据我们的需求，通过代码来实现它的功能）
3. 运行代码
4. 修复和完善

### 提出需求

获取 [豆瓣电影 Top 250](https://movie.douban.com/top250?start=0) 的内容
要求：
* 获取电影名称、上映日期、评分
* 写入文本文件

request

urllib 模拟浏览器的第三方库

Beautiful Soup 是一个可以从HTML或XML文件中提取数据的Python库

推导式写法：
```python
tuple(f'https://movie.douban.com/top250?start={ page * 25 }&filter=' for page in range(10))
```

展开：
```python
a = []
for page in range(10):
    pages = f'https://movie.douban.com/top250?start={ page * 25 }&filter='
    a.append(pages)
tuple(a)
```

## 爬虫工程师必备的 HTML 基础

1. HTTP 协议与浏览器的关系
2. HTTP 协议请求与返回头部
3. HTTP 请求方式 get post delete head put
4. HTTP 状态码
5. W3C 标准
6. HTML 常用标签和属性
7. CSS Javascript Json 简介

scrapy 新建项目步骤

```shell
scrapy startproject spiders
cd spiders/
scrapy genspider movies movie.douban.com
```
dont_filter=ture 的时候开启调试，或者允许多域名爬虫

 ### XPATH 语法

 // 匹配任意长的路径
