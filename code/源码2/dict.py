# 字典类型={键:值} 由 键值对 组成
# key                    value
# 唯一                    不唯一
# 不可变                   可变
# 不可变数据类型:        任何数据类型
# 字符串、数字、元组

dict1 = {"name": "Tom",
         "age": 18,
         "class": 3}
# 通过键来访问值
print(dict1["name"])
print(dict1["age"])

# 修改值
dict1["age"] = 19
print(dict1["age"])

# 添加
dict1["gender"] = "Male"
print(dict1)

# 删除元素
'''
del dict1["age"]
print(dict1)
dict1.clear()
print(dict1)
del dict1
# print(dict1) 访问异常
'''

# 函数和方法
print(len(dict1))  # key的个数
#print(str(dict1))

dict2 = dict1.copy()
print(dict2)
dict1["gender"] = "Female"
print(dict1)
print("dict2",dict2)

tup=("Name","Age","Class")
tup_value=(1,2,3)
print(tup)
dict3=dict1.fromkeys(tup,"warning")
print(dict3)
dict3["name"]="Tom"
print("dict3:",dict3)

# 查找键的值
print(dict1.get("name"))

print(dict1.items()) # 以列表返回可遍历的（键，值）元组
print(dict1.keys()) # 返回所有键
print(dict1.values()) # 返回所有值

dict1.setdefault("school") # 与get()类似，不存在键时，自动添加，并将值设为defaut
print(dict1)
dict1["school"]="GDUT"
print(dict1)

dict2.update(dict1) # 把dict1的键值对更新到dict2里
print("dict2",dict2)

print(dict2.pop("name")) # 按 键删除并返回对应的值，必须给出键，否则返回Default值
print(dict2)
print(dict2.popitem()) # 删除并返回最后一对键值
print(dict2)