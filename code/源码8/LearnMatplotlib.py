'''
matplotlib学习
折线图 plot 趋势随时间变化
柱状图/条形图 bar 类别之间对比
饼图 pie 整体组成比例
散点图 scatter 两变量相关性
箱线图 boxplot 观察数据分布，异常值
'''

import matplotlib.pyplot as plt
from nltk.misc.chomsky import subjects

# 设置中文字体
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['SimHei']


# 创建图表,设置大小
plt.figure(figsize=(10,10))
'''
month=['1月','2月','3月',
       '4月','5月','6月',
       '7月','8月','9月',
       '10月','11月','12月']

sales=[100,150,80,
       130,120,150,
       180,200,140,
       160,171,190,]
# 折线图
plt.plot(month,sales,
         label='产品A',
         color='orange',
         linewidth=2,
         linestyle='--',
         marker='o',)

# 其他参数配置
# 添加标题
plt.title('2025年销售趋势',color='red',fontsize=20)
# 添加坐标轴的标签
plt.xlabel('月份',fontsize=20)
plt.ylabel('销售额（万元）',fontsize=20)

# 添加图例
plt.legend(loc='upper left',fontsize=20  )

# 添加网格线
#plt.grid(True) # xy两条轴都有
plt.grid(axis='y',linestyle='--',linewidth=0.5) # y轴有
plt.grid(axis='x',linewidth=0.5,color='red') # x轴有

# 设置刻度字体大小
plt.xticks(rotation=0,fontsize=20)
plt.yticks(rotation=0,fontsize=15)

# 设置y轴显示范围
plt.ylim([0,300])

# 在每个数据点上显示数值
for x,y in zip(month,sales):
       plt.text(x,y,str(y),fontsize=20,ha='center',va='center')


# 柱状图
subjects = ['语文','数学','英语','科学']
scores = [100,150,80,130]
# 绘制柱状图
plt.bar(subjects,scores,
        label='小米',
        color='orange',
        width=0.4,)

plt.title('小米2025年成绩',color='red',fontsize=20)
plt.xlabel('subject',fontsize=20)
plt.ylabel('score',fontsize=20)

plt.legend(loc='upper left',fontsize=20)
plt.grid(axis='y',alpha=0.1,linestyle='--',linewidth=1)

plt.xticks(rotation=0,fontsize=20)
plt.yticks(rotation=0,fontsize=15)
plt.ylim([0,160])

for x,y in zip(subjects,scores):
        plt.text(x,y,str(y),fontsize=20,ha='center',va='center')

# 条形图:排名的时候或者名字比较长的时候
subjects = ['语文','数学','英语','科学']
scores = [100,150,80,130]

plt.barh(subjects,scores,
        color='orange',
        width=0.4,))

# 饼图:最好不要超6类
things = ['学习','娱乐','运动','睡觉','其他']
times = [6,4,1,8,5]
# 配色
colors = ['#66b3ff','#99ff99','#ffcc99','#ff4499','#ff9999']
# 绘图
plt.pie(times,
        labels=things,
        autopct='%1.1f%%', # 显示百分比
        colors=colors, # 设置配色
        )

# 添加标题
plt.title('一天时间分布',color='red',fontsize=20)

# 环形图
things = ['学习','娱乐','运动','睡觉','其他']
times = [6,4,1,8,5]
# 配色
colors = ['#66b3ff','#99ff99','#ffcc99','#ff4499','#ff9999']
# 绘图
plt.pie(times,
        labels=things,
        autopct='%1.1f%%', # 显示百分比
        colors=colors, # 设置配色
        wedgeprops={'width':0.7,}, #(1 - 小圆半径)/大圆半径
        pctdistance=0.6, # 设置百分数的位置
        )
plt.text(0,0,'总计：\n100%',
         ha='center',va='center',fontsize=20)





# 添加标题
plt.title('一天时间分布',color='red',fontsize=20)


# 绘制爆炸式饼图
things = ['学习','娱乐','运动','睡觉','其他']
times = [6,4,1,8,5]
# 配色
colors = ['#66b3ff','#99ff99','#ffcc99','#ff4499','#ff9999']
explode = [0.1,0,0,0,0] # 设置爆炸参数


# 绘图
plt.pie(times,
        labels=things,
        autopct='%1.1f%%', # 显示百分比
        colors=colors, # 设置配色
        explode=explode,
        )

# 添加标题
plt.title('一天时间分布',color='red',fontsize=20)


#  散点图
import random
# 要绘制的数据
x = []
y = []

for i in range(1000):
    tmp = random.uniform(0,10)
    x.append(tmp)
    tmp2 = 2*tmp + random.gauss(0,2)
    y.append(tmp2)

scores = [50,55,60,65,70,75,80]
hours = [1,2,3,4,5,6,7]

# 绘制散点图
plt.scatter(x,y,
            color='blue',
            alpha=0.5,
            s=20,
            label='数据',)

# 添加标题
plt.title('x-y',color='red',fontsize=20)
# 添加坐标轴的标签
plt.xlabel('x轴',fontsize=20)
plt.ylabel('y轴',fontsize=20)

# 添加图例
plt.legend(loc='upper left',fontsize=20  )

# 添加网格线
#plt.grid(True) # xy两条轴都有
plt.grid(axis='y',linestyle='--',linewidth=0.5) # y轴有
plt.grid(axis='x',linewidth=0.5,) # x轴有

plt.ylim([0,30])
plt.plot([0,10],[0,20],color='red',linewidth=2 )
# 设置刻度字体大小
plt.xticks(rotation=0,fontsize=20)
plt.yticks(rotation=0,fontsize=15)

# 箱型图
data = {
    '语文':[75,78,76,80,86,85,89,95,90,88],
    '数学':[98,95,75,86,85,94,77,88,40,89],
    '英语':[77,55,99,65,85,67,86,87,96,76]
}

plt.boxplot(data.values(),tick_labels=data.keys())

plt.title('各科成绩箱线图',color='red',fontsize=20)
plt.ylabel('分数',fontsize=20)
plt.grid(True,linestyle='--',linewidth=0.5,axis='y')
'''

# 直方图
#plt.hist(画图的变量,bins=5) # 自动分箱，bins分成5段


# 动态图表生成

month=['1','2','3',
       '4','5','6',
       '7','8','9',
       '10','11','12']

sales=[100,150,80,
       130,120,150,
       180,200,140,
       160,171,190,]

f1 = plt.subplot(2,2,1)
f1.plot(month,sales)
f2 = plt.subplot(2,2,2)
f2.bar(month,sales)
f3 = plt.subplot(2,2,3)
f3.scatter(month,sales)
f4 = plt.subplot(2,2,4)
f4.barh(month,sales)

# 自动优化排版
plt.tight_layout()

# 显示图表
plt.show()