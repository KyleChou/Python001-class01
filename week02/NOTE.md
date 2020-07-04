学习笔记

## 异常捕获与处理

捕获异常提升了程序的健壮性

### 异常处理机制的原理

* 异常也是一个类 （Traceback 类）
* 异常捕获过程
1. 异常类把错误消息打包到一个对象
2. 然后该对象会自动查找到调用栈
3. 直到运行系统找到明确声明如何处理这些类异常的位置
* 所有异常继承自 BaseException
* Traceback 显示了出错的位置，显示的顺序和异常信息对象传播的方向是相反的

### 异常信息与异常捕获

* 异常信息在 Traceback 信息的最后一行，有不同的类型
* 捕获异常可以使用 try...except 语法
* try...except 支持多重异常处理

常见的异常类型主要有
1. LookupError 下的 IndexError 和 KeyError
2. IOError
3. NameError
4. TypeError
5. AttributeError
6. ZeroDivisionError

> **尝试进行复现上述异常**

自定义一个异常的时候，要从类 Exception 继承
```python
class UserInputError(Exception):
    pass
```

try...exception...finally finally后面语句不管前面什么情况，都会去执行

pretty_errors 模块对异常的输出进行美化

类中 __xx__ 双下划线函数称为魔术方法

## 使用 PyMySQL 进行数据库操作

建议  3.7 版本以上的 python 使用 PyMySQL 连接 MySQL 数据库

## 

### 浏览器基本行为

1. 带 http 头信息：如 User-Agent、Referer 等（搜索浏览器 Header 大全）
2. 带cookies（包含加密的用户名、密码验证信息）