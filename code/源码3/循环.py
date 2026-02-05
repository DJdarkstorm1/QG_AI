# for循环可以遍历序列（列表、元组、字符串）
# 但不可以遍历集合

# 生成函数 range(start,stop,step=1)
# 降序生成时step要负数
for i in range(1,10):
    print(i)

for i in range(1,10,2):
    print(i)

for i in range(10,1,-2):
    print(i)

# for 的else子语句：False 时执行，如果break就不执行
for i in range(1,10,2):
    print(i)
    if i>5:
        break
else:
    print("end")

# while 的else子语句：False 时执行，如果break就不执行
i=0
while i<5:
    print(i)
    i=i+1
    if i>3:
        break
else:
    print("i不小于5")

# continue
for i in range(1,10):
    if i%2==0:
        continue
    print(i)