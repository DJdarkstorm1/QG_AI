# 函数
"""函数定义与命名(注意冒号)"""
from enum import global_enum

from six import print_


def fun1():
    print("这是一个测试函数1")

fun1()
# 规范命名，见名知意：小写加下划线
def add(x,y):
    """
    复杂的函数要写注释，解释函数功能
    :param x:一个加数
    :param y: 另一个加数
    :return: x+y的和
    """
    return x+y

print(add(1,2))

# 暂时没写的函数
def not_do_yet():
    pass
print(not_do_yet())

"""参数"""
# 位置参数：要按顺序传入参数
def minus(x,y):
    return x-y
print(minus(1,2))

# 关键字参数:按关键字给参数，不必按顺序
print(minus(y=3,x=4))

# 默认参数：默认参数放在最后，默认参数必须执行不变的对象
def printme(x,y=6):
    print(x,y)
    return
printme(1)
printme(2,3)

# 不定长参数/可变参数：
# 不定长位置参数：*args(参数会被打包成一个元组)
def sum_num(*args):
    print(type(args))
    print(sum(args))
    return
sum_num(1,2,3,4,5,6)

# 不定长关键字参数:**kwargs(参数被打包成一个字典)
def info_system(**kwargs):
    print(type(kwargs))
    print(kwargs)
    return
info_system(name="Tom",age=18)

"""
参数声明必须按以下顺序
1.位置参数
2.默认参数
3.*args
4.仅关键字参数
5.**kwargs
例如：
"""
def example(
        pos1,
        pos2,
        def1=1,
        def2=2,
        *args,
        key_only1=True,
        key_only2=False,
        **kwargs,
):
    print(pos1,pos2,def1,def2,key_only1,key_only2)
    print(args)
    print(kwargs)
    return

"""参数传递"""
# 传递不可变类型（string tuple number）:类似C++的值传递
# 传递可变类型（list dict）:类似C++的引用传递

"""返回值"""
# 单个返回值
def one(x):
    print("返回一个返回值")
    return x+1
print(one(1))

# 返回多个返回值 会被打包成元组返回
def two(x):
    print("返回2个返回值")
    return x+1,x
print(two(3))

def three(x):
    print("返回3个返回值")
    return x*2,x+2,x
print(three(3))
# 也可以用多个变量接收（解包）
a,b,c=three(3)
print(a,b,c)

"""作用域（例程）"""
global_num=100

def outer():
    # 嵌套作用域
    enclosing_num=10
    def inner():
        # 局部作用域
        local_num=1
        print(local_num) # 先在局部作用域找到local_num
        print(enclosing_num) # 局部作用域没有，到嵌套作用域找
        print(global_num) # 局部和嵌套作用域都没有，到全局作用域找
        print(len([1,2,3])) # 前面都没找到，到内置作用域找
    inner()

outer()
"""
变量名查找顺序（LEGB规则）
Local 局部
Enclosing 嵌套
Global 全局
Built-in 内置
若在内置中找不到，就会抛出NameError异常
"""

"""匿名函数"""
# lambda 参数，参数：表达式（只能一条）
add=lambda a,b:a+b
print(add(1,2))

# 常见用法1
multiply=lambda a,b:a*b
print(multiply(3,4))

# 将匿名函数赋值给其他函数替换其他函数的功能/功能屏蔽（mock）
fun1()
fun1=lambda x,y:x*y
print(fun1(6,6))
fun1=lambda x:None
print(fun1(1))

# 作为参数传递
def lambda_test(x,y,func):
    print(func(x,y))

lambda_test(1,2,lambda x,y:x*y)


"""练习"""
# 改造下面代码
# ---------------
def judge_odd(n):
    return n%2==1
L=list(filter(judge_odd,range(1,10)))
print(L)
# ---------------
L1=list(filter(lambda n:n%2==1,range(1,10)))
print(L1)

"""嵌套函数"""
def counter():
    count=100
    def change_count():
        nonlocal count
        if count<0:
            count=0
        current=count
        count-=1
        return current
    return change_count

c=counter()

for count in range(0,105):
    print(c())

"""
高阶函数：能接受函数作为参数，或能返回函数作为结果的函数
"""



