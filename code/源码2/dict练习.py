# 合并以下两个学生字典，
# 如果有学生重复，则最终成绩为二者相加

dict_stu1={"A":90,"B":85,"C":78,"D":60}
dict_stu2={"F":88,"C":92,"B":15}
'''

for key1,value1 in dict_stu1.items():
    for key2,value2 in dict_stu2.items():
        if key1==key2:
            val=value1+value2
            dict_stu2[key2]=val
dict_stu3=dict_stu1.copy()
dict_stu3.update(dict_stu2)
print("三",dict_stu3)
'''
# 更优解
dict_stu4=dict_stu1.copy()
for key1,value1 in dict_stu2.items():
    if key1 in dict_stu1:
        dict_stu4[key1]+=value1
    else:
        dict_stu4[key1]=value1

print("四",dict_stu4)