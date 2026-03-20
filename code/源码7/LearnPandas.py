'''
数据分析步骤
1.导入必要的库
2.导入数据
3.数据清洗：缺失值的处理，
4.数据特征构造：分组，分箱
5.数据分析
'''

# 数据分析处理
# 数据导入
from sympy.parsing.maxima import var_name

import pandas as pd
import numpy as np
'''
# df = pd.read_csv('./加州房价.csv')
print("导入成功")


# 缺失值的处理
s = pd.DataFrame([[1,2,np.nan,None,pd.NA],
               [np.nan,1,2,None,pd.NA],
               [4,5,np.nan,None,6]],columns=['a','b','c','d','e'])
#print(s)

# 查看是否是缺失值
#print(s.isna())
#print(s.isnull())
# 剔除缺失值
#print(s.dropna()) # 删一整行
#print(s.dropna(how='all')) #如果所有值都是缺失值，删除这一行
#print(s.dropna(thresh=2)) #如果至少有n个值不是缺失值，就保留
#print(s.dropna(axis=1)) # 删一整列
#print(s.dropna(subset=['a'])) # 如果某列有缺失值，则删除这一行
#print(s.dropna(subset=['b']))

# 填充缺失值
# print(s.fillna({'a':9})) #使用字典来填充
#print(s.fillna(s[['a']].mean())) # 使用平均值填充
#print(s.ffill()) # 用前面相邻的值填充
#print(s.bfill()) # 用后面相邻的值填充

# 重复值处理
data = {
    "name":['a','a','b','c','b','a'],
    "age":['26','25','30','25','30','26'],
    "city":['NY','NY','LA','SF','LA','NY']
}
df= pd.DataFrame(data)
print(df)
# 检测重复数据
#print(df.duplicated()) # 一整条数据都一样，标记为重复，返回True
#print(df.drop_duplicates())
#print(df.drop_duplicates(subset=['city'])) #按指定列去重
#print(df.drop_duplicates(subset=['name'], keep='first')) # 保留第一次出现的数据去重
#print(df.drop_duplicates(subset=['city'], keep='last')) # 保留最后一次的数据

# 数据类型的转换:方便继续处理
df = pd.read_csv('./加州房价.csv')
print("导入成功")
print(df.head())
print(df.dtypes)
df['total_rooms'] = df['total_rooms'].astype(int)
print(df.dtypes)


# 数据变形
data = {
    "id":[1,2,3],
    "name":['a','b','c'],
    "math":[89,98,78],
    "English":[78,79,98],
    "Science":[78,77,88]
}
df = pd.DataFrame(data)
print(df)

# 宽表 转换成 长表
df2 = pd.melt(df,id_vars=['id','name'],
              var_name='科目',
              value_name='分数')
print(df2)

print(df2.sort_values('name'))

# 长表转宽表
df3 = pd.pivot(df2,index=['id','name'],
               columns='科目',
               values='分数')
print(df3)

# 数据分列
data = {
    "id":[1,2,3],
    "name":['a smith','b green','c galler'],
    "math":[89,98,78],
    "English":[78,79,98],
    "Science":[78,77,88]
}
df = pd.DataFrame(data)
df[['first_name','last_name']] = df['name'].str.split(" ", expand=True) # expand=True自动分列
print(df)

# 数据分箱
# 字符串-->类别（category）-->统计
# 数值  -->分箱           -->统计
df = pd.read_csv('./加州房价.csv')
print("导入成功")
df1=df.head(10)[['total_rooms','total_bedrooms','population']]
print(df1)
# print(pd.cut(df1['population'],bins=3).value_counts()) #bins=n分n段
# print(pd.cut(df1['population'],bins=[0,500,1500,3000])) #bins=list自定义区间
# print(pd.cut(df1['population'],bins=[0,500,1500,3000],labels=['低','中','高']))

df1['受欢迎程度'] = pd.cut(df1['population'],bins=[0,500,1500,3000],labels=['低','中','高'])
print(df1)
print(df1['受欢迎程度'].dtype)

# 等分
#print(pd.qcut(df1['population'],3).value_counts())

# 其它操作
df2=df1
print(df2.set_index('受欢迎程度',inplace=True)) # inplace=True对当前的df生效，False对当前的df不生效
df2.reset_index(inplace=True)
df2.rename(columns={'population':'人气值'},index={0:10},inplace=True)
df2.index=[1,2,3,4,5,6,7,8,9,10] # 要改就要全改
print(df2)

# 时间类型
d = pd.Timestamp('2025-12-31 12:30')
print(d)
print(type(d))
print("年：",d.year)
print("月：",d.month)
print("日：",d.day)
print("时：",d.hour)
print("分：",d.minute)
print("秒：",d.second)
print("季度：",d.quarter)
print("是否月底",d.is_month_end)
print("星期几",d.day_name())
print("转化为天",d.to_period("D"))
print("转化为季度",d.to_period("Q"))
print("转化为周维度",d.to_period("W"))

# 字符串转换为日期类型
a = '2025-12-09'
b = pd.to_datetime(a)
print(b)
print(type(b))
print(b.day_name())

# dataframe日期转换
df = pd.DataFrame({
    'date':[20251201,20251202,20251203,20251204,20251205],
    'sales':[100,200,300,400,500],
    'saler':['a','b','c','d','e']
})
print(df)
#df['datetime'] = pd.to_datetime(df['date']) # 时间格式换算不对
# 正确的转换方式：先转字符串 + 指定日期格式
df['datetime'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
print(df)
print(df.dtypes)
df['weekday'] = df['datetime'].dt.day_name() #取时间要加 dt.
print(df)

# csv 导入时进行日期转换
#df = pd.read_csv('./XXX.csv',parse_dates=['date'])

# 将日期作为索引
#df.set_index('datetime',inplace=True)
#print(df)
# 可以按时间切片
print(df.loc['2025-12-02':'2025-12-04'])
# 时间间隔
d1=pd.Timestamp('2006-12-09')
d2=pd.Timestamp('2026-03-08 ')
d3=d2-d1
print(d3)
print(type(d3)) # 时间间隔类型
# 时间间隔作为索引
df['delta'] = df['datetime']-df['datetime'][0]
df.set_index('delta',inplace=True)
print(df)
# 可以继续切片了
print(df.loc['2 days':'4 days'])

# 生成时间戳
days = pd.date_range(start='2025-12-09', end='2026-03-08', freq='W') # 以周为频率
days1 = pd.date_range(start='2025-12-09', periods=10, freq='W') # periods=n 取n个
print(days1)

# 重新采样
# 将重采样的日期作为索引
df.set_index('datetime',inplace=True)
# 设置重采样对象
df[['sales']].resample('W').sum()
print(df[['sales']].resample('W').sum())
'''
# 分组聚合
# df.groupby('分组的字段')['聚合的字段'].聚合函数()
# 多个参数分组
# df.groupby(['分组的字段1','分组的字段2'])['聚合的字段'].聚合函数()
df = pd.read_csv('./加州房价.csv')
print("导入成功")
#df = df.head(50)
print(df.groupby('ocean_proximity').groups)
print(df.groupby('ocean_proximity').get_group('<1H OCEAN'))
df2 = df.groupby('ocean_proximity')[['median_house_value']].mean()
df2['median_house_value'] = df2['median_house_value'].round(2)
df2.sort_values('median_house_value', inplace=True)
print(df2)
#print(df)
# 数据导出
# df.to_csv('./new.csv')
print("导出成功")