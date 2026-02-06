"""封装"""
'''
现实事物            类
属性    ->        成员变量
行为    ->        成员行为
'''

# 私有成员变量/方法：以__开头,
# 外部不能直接访问，
# 内部函数可以直接访问，只能通过内部函数间接访问
class Phone:
    id = None
    brand = None

    __current_voltage = 1 # 当前手机电压

    def call_me(self):
        print(f"hello,this is {self.brand} phone")

    def __back_run_app(self):
        print(f"后台运行程序关闭")

    def light_up(self):
        if self.__current_voltage > 2:
            print("闪光灯已打开")
        else:
            self.__back_run_app()
            print("电量不足，无法使用闪光灯")
'''
phone = Phone()
phone.brand="HUAWEI"
phone.call_me()
phone.__current_voltage = 20 # 调用无效
# phone.__back_run_app() # 调用报错
phone.light_up()
'''
# 练习题

class MobilePhone:
    __is_5G_enable = True
    def __check_5g(self):
        if self.__is_5G_enable:
            print("5g开启")
        else:
            print("5g关闭，使用4g网络")
    def call_by_5g(self):
        self.__check_5g()
        print("正在通话中")

phone1 = MobilePhone()
phone1.call_by_5g()


