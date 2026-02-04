import cmp
'''
list1=[1,2,3,4,5,"hello","world","你好","世界"]
# 访问方式
# 单个元素访问
print(list1[0])
print(list1[-1])
# 多个元素访问[起始索引（0）:结束索引（Length）:步长]
print(list1[::])
print(list1[2::])
print(list1[:2:])
print(list1[::2])
print(list1)
# 修改列表
list1[0]="修改列表"
list1.append("hi")
print(list1)
list1.insert(1,"呵呵呵")
print(list1)
list1.extend(["ex1","ex2"])
print(list1)
# 删除
list1.remove("ex1") # 删除第一个匹配的元素
print(list1)
print(list1.pop()) # 删除并返回元素，默认最后一个
print(list1)

del list1[2] #删除指定索引的元素
print(list1)
list1.clear() # 清空
print(list1)

# 列表脚本操作符
list2=[1,2,2]+[3,4,5,] # 组合
print(list2)
list3=["呵"]*3 # 重复
print(list3)
a=3 in list2 # 判断元素是否存在于列表中
print(a)
for i in list3: # 迭代/遍历
    print(i)
'''
# 函数


# 方法
list4=[1,1,1,2,2,3]
print(list4.count(1))
print(list4.count(2))
list4.reverse()
print(list4)
list5=[5,3,4,9,8,1,6,2,5]
list5.sort(reverse=True) # 默认升序，True为降序
print(list5)
print(len(list5))
print(max(list5))
print(min(list5))