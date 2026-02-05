# 列表 推导式
# 1
sqtr_list=[x**2 for x in range(1,11)]
print(sqtr_list)

# 2
members_list=["张三","李四","王五"]
# QG_member_list=[f"QG_{x}" for x in members_list]
QG_member_list=list(map(lambda x:f"QG_{x}",members_list))
print(QG_member_list)

# 3
numbers=[1,2,3,4,5,6,7,8,9]
plus=lambda x : x+10
plus_numbers=[plus(x) for x in range(10)]
print(plus_numbers)

# 4
words=["a","b","c"]
# upper_words=list(map(lambda x:x.upper(),words))
upper_words=[x.upper() for x in words]
print(upper_words)