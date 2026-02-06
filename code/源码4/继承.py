"""继承"""

class Phone:
    id = None
    brand = "HUAWEI"

    def call_by_4g(self):
        print("4g通话")

class Phone2025(Phone):
    version = 2025
    face_id = True

    def call_by_5g(self):
        print("5g通话")

phone = Phone2025()
phone.call_by_4g()
phone.call_by_5g()
print(phone.version)

class NFCReader:
    nfc_type = "version1"
    brand = "HM"

    def read_card(self):
        print("NFC读卡")

    def write_card(self):
        print("NFC读卡")

class Inferred:
    ir_type = "version2"
    brand = "HM"

    def send_msg(self):
        print("红外发送信息")

    def recieve_msg(self):
        print("红外接收信息")

class Phone2026(Phone, Inferred, NFCReader):
    pass # 不添加功能函数就pass

phone2 = Phone2026()
phone2.call_by_4g()
phone2.write_card()
phone2.recieve_msg()
phone2.send_msg()
phone2.read_card()
# 访问同名的成员属性时，优先级按继承顺序
print(phone2.brand)

# 复写
class Phone2027(Phone, Inferred, NFCReader):
    version =2027
    brand = "Honor" # 复写父类的属性
    # 复写父类的方法
    def call_by_5g(self):
        print("子类的5g通话")
        # 在子类中调用父类的方法/属性
        print(f"父类的品牌：{Phone.brand}")
        Phone.call_by_4g(self)
        print(super().brand)
        super().call_by_4g()
        print("---父类结束---")

phone3 = Phone2027()
phone3.call_by_4g()
phone3.call_by_5g()
print(phone3.version)
print(phone3.brand)