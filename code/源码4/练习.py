from networkx.algorithms.distance_measures import radius


class Shape:
    shape_counter = 0

    __area = 0.0

    def __init__(self):
        self.__area = 0.0
        Shape.shape_counter += 1

    def __calc_area(self):
        pass



    def get_counter(self):
        return Shape.shape_counter

class Circle(Shape):
    radius = 0

    def __init__(self,radius):
        self.radius = radius
        Shape.__init__(self)

    def __calc_area(self):
        self.__area = 3.14*(self.radius**2)

    def get_area(self):
        self.__calc_area()
        return self.__area

class Rectangle(Shape):
    width = 0
    height = 0
    def __init__(self,width,height):
        self.width = width
        self.height = height
        Shape.__init__(self)

    def __calc_area(self):
        self.__area = self.width*self.height

    def get_area(self):
        self.__calc_area()
        return self.__area

r1=Circle(5)
print(r1.get_area())
print(r1.get_counter())

r2=Rectangle(5,5)
print(r2.get_area())
print(r2.get_counter())
'''
"""str.strip()用法示例"""
def test_str_strip():
    """
    验证str.strip()的默认行为和隐含特性
        只会删除前导和末尾的匹配 字符串里的单个字符 的字符，不是整个字符串去匹配
    """
    print("===== str.strip() 文档验证 =====")
    # 文档示例
    comment_string = '#....... Section 3.2.1 Issue #32 .......'
    result=comment_string.strip('.#! ')
    print(f"原始字符串：{repr(comment_string)}")
    print(f"strip后：{repr(result)}")

    # 测试用例1：默认删除首尾所有空白字符（空格、换行、制表符等）
    test_str1 = "  abc  \n\t123 \n "
    result1 = test_str1.strip()
    print(f"\n原始字符串：{repr(test_str1)}")
    print(f"strip后：{repr(result1)}")  # repr()显示特殊字符，更直观

    # 测试用例2：指定删除字符（验证非空白场景）
    test_str2 = "###abc###123###"
    result2 = test_str2.strip("#")
    print(f"\n原始字符串：{repr(test_str2)}")
    print(f"strip('#')后：{repr(result2)}")

    # 测试用例3：空字符串场景
    test_str3 = "  "
    result3 = test_str3.strip()
    print(f"\n空字符串strip后：{repr(result3)}")
'''