# 集合特点：无序，不重复
# 不能通过下标访问
# 创建方法
from sympy.sets.handlers.union import union_sets

set1={1,9,6,4,4,5} #会自动除重
set2= set([5,6]) # 创建空集合时必须用set()
                 # {}是用来创建字典的
print(set1)
print(set2)

# 访问
for i in set1:
    print(i)

print(1 in set1)
print(0 in set1)

set2.add(5) # 添加以有元素，不进行任何操作
print(set2)
set2.add(9) # 只添加不存在的元素
print(set2)

set2.update([8,7])
# 参数可以是list tuple dict 也可以是单个元素
print(set2)

# 删除
set2.remove(9) # 从集合中移除指定元素 如果元素不存在 会报错 但编译器不会提示
print(set2)
set2.discard(9) # 不会报错
print(set2)
set2.pop() #随机删除一个元素（无序）
print(set2)

# 运算
# 并集
union_set=set1|set2
print("并集",union_set)

union_set=set1.union(set2)
print(union_set)

# 交集
intersection_set=set1.intersection(set2)
print("交集",intersection_set)

intersection_set=set1&set2
print(intersection_set)

# 差集
difference_set=set1-set2
print("差集",difference_set)

difference_set=set1.difference(set2)
print(difference_set)

# 对称差集:两集合不重复的元素
symmetric_set=set1.symmetric_difference(set2)
print("对称差集",symmetric_set)
symmetric_set=set1^set2
print(symmetric_set)