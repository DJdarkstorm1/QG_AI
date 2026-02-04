# 元组不能修改已有的元素
tup=(1,2,1,30,"hello")
tup1=() # 可以创建空元组


tup2=(0,) # 单个元素的元组要加逗号
tup3=(1)
print(type(tup2)) # <class 'tuple'>
print(type(tup1)) # <class 'tuple'>
print(type(tup3)) # <class 'int'>

# 可以没有圆括号
tup4='abc',3.14,"hello"
print(tup4)

# 访问元组
print(tup4[1])
print(tup4[:2]) # 切片/截取元组 [起始索引:结束索引:步长]

# 修改元组
tup_num=1,2,2,3,3,3
tup_str="hello","world",
tup5= tup_num + tup_str
print(tup5)

# 不能删除/修改元素 但可以删除元组
del tup5
# print(tup5) # tup5无法访问

# 运算符（同列表）
print(len(tup_num))
tup5="呵"*3
print(tup5)

# 函数和方法
# cmp(tup_num,tup5) # 有BUG
len_tup5=len(tup5)
print(len_tup5)
print(max(tup_num))
print(min(tup_num))
print(tup_num.count(2))
print(tup4.index(3.14))
