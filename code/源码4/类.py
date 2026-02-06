# 类
class Student(object):
    # 属性
    name = None
    gender = None
    nationality = None
    native_place = None
    age = None
    def __init__(self,name,gender,nationality,native_place,age):
        self.name = name
        self.gender = gender
        self.nationality = nationality
        self.native_place = native_place
        self.age = age

    def __str__(self):
        return str(self.name)

    # 方法
    def say_hi(self):
        print(f"Hello I am {self.name}")

    def say_hi_msg(self,msg):
        print(f"Hello I am {self.name}.{msg}")

    def get_msg(self):
        print(self.name)
        print(self.gender)
        print(self.nationality)
        print(self.native_place)
        print(self.age)

# 创建对象并初始化
stu1=Student("呵呵呵","male","China","Guangdong",18)              #创建对象

# 对象属性进行赋值

# 获取对象信息

stu1.get_msg()
stu1.say_hi()
stu1.say_hi_msg("I am Chinese.")
print("__str__方法",stu1)





