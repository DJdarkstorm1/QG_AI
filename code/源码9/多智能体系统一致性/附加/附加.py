import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# ===================== 地图数据 =====================
points = [
    {"name":"松风涧","x":4690,"y":330,"type":0},
    {"name":"月栖滩","x":5360,"y":770,"type":0},
    {"name":"云岫台","x":3280,"y":1920,"type":0},
    {"name":"花溪渡","x":3680,"y":2090,"type":0},
    {"name":"星垂浦","x":4670,"y":2160,"type":0},
    {"name":"竹影潭","x":5670,"y":2230,"type":0},
    {"name":"雾隐桥","x":1820,"y":3310,"type":0},
    {"name":"棠香坞","x":2790,"y":3330,"type":0},
    {"name":"枫径斜","x":3210,"y":3380,"type":0},
    {"name":"荷风榭","x":4190,"y":3110,"type":0},
    {"name":"砚池春","x":4740,"y":3180,"type":0},
    {"name":"书声崖","x":5380,"y":3200,"type":0},
    {"name":"画舫驿","x":6020,"y":3310,"type":0},
    {"name":"棋趣坪","x":1950,"y":3840,"type":0},
    {"name":"诗墙巷","x":2840,"y":3930,"type":0},
    {"name":"灯影廊","x":3280,"y":3880,"type":0},
    {"name":"拓片台","x":3680,"y":4150,"type":0},
    {"name":"弦歌榭","x":4160,"y":4110,"type":0},
    {"name":"忆旧轩","x":4690,"y":4190,"type":0},
    {"name":"问津亭","x":4690,"y":3820,"type":0},
    {"name":"雀跃坪","x":5400,"y":3770,"type":0},
    {"name":"蝶踪径","x":6000,"y":3750,"type":0},
    {"name":"萤火星","x":3280,"y":4680,"type":0},
    {"name":"风铃渡","x":3570,"y":5080,"type":0},
    {"name":"落英阶","x":4300,"y":4880,"type":0},
    {"name":"镜心湖","x":5270,"y":4750,"type":0},
    {"name":"踏浪矶","x":2370,"y":5740,"type":0},
    {"name":"叠翠屏","x":2480,"y":6250,"type":0},
    {"name":"听雪轩","x":3240,"y":6090,"type":0},
    {"name":"陆小凤","x":4520,"y":5900,"type":0},
    {"name":"小凤路","x":5930,"y":5670,"type":0}
]

edges = [
    {"name":"店前路","start_id":0,"end_id":1,"limit_speed":6.94,"degree":3},
    {"name":"和平路","start_id":0,"end_id":2,"limit_speed":6.94,"degree":3},
    {"name":"幸福街","start_id":1,"end_id":5,"limit_speed":6.94,"degree":3},
    {"name":"光明道","start_id":2,"end_id":6,"limit_speed":6.94,"degree":3},
    {"name":"健康巷","start_id":2,"end_id":3,"limit_speed":6.94,"degree":3},
    {"name":"东风路","start_id":3,"end_id":4,"limit_speed":6.94,"degree":3},
    {"name":"朝阳街","start_id":4,"end_id":5,"limit_speed":6.94,"degree":3},
    {"name":"民生路","start_id":6,"end_id":7,"limit_speed":6.94,"degree":3},
    {"name":"自由街","start_id":6,"end_id":13,"limit_speed":6.94,"degree":3},
    {"name":"建国路","start_id":3,"end_id":7,"limit_speed":6.94,"degree":3},
    {"name":"厂边路","start_id":7,"end_id":8,"limit_speed":6.94,"degree":3},
    {"name":"湾仔道","start_id":7,"end_id":14,"limit_speed":6.94,"degree":3},
    {"name":"新华道","start_id":5,"end_id":12,"limit_speed":6.94,"degree":3},
    {"name":"友谊巷","start_id":4,"end_id":11,"limit_speed":6.94,"degree":3},
    {"name":"团结街","start_id":3,"end_id":9,"limit_speed":6.94,"degree":3},
    {"name":"创新道","start_id":8,"end_id":9,"limit_speed":6.94,"degree":3},
    {"name":"菜场巷","start_id":9,"end_id":10,"limit_speed":6.94,"degree":3},
    {"name":"坝上街","start_id":10,"end_id":11,"limit_speed":6.94,"degree":3},
    {"name":"山脚下","start_id":10,"end_id":19,"limit_speed":6.94,"degree":3},
    {"name":"坡底路","start_id":11,"end_id":12,"limit_speed":6.94,"degree":3},
    {"name":"桥南街","start_id":11,"end_id":20,"limit_speed":6.94,"degree":3},
    {"name":"河滨道","start_id":12,"end_id":21,"limit_speed":6.94,"degree":3},
    {"name":"村头路","start_id":8,"end_id":15,"limit_speed":6.94,"degree":3},
    {"name":"奋进路","start_id":13,"end_id":14,"limit_speed":6.94,"degree":3},
    {"name":"迎宾道","start_id":13,"end_id":26,"limit_speed":6.94,"degree":3},
    {"name":"岗头巷","start_id":14,"end_id":15,"limit_speed":6.94,"degree":3},
    {"name":"丰收街","start_id":14,"end_id":22,"limit_speed":6.94,"degree":3},
    {"name":"学堂路","start_id":15,"end_id":16,"limit_speed":6.94,"degree":3},
    {"name":"巷尾街","start_id":16,"end_id":17,"limit_speed":6.94,"degree":3},
    {"name":"六里街","start_id":17,"end_id":18,"limit_speed":6.94,"degree":3},
    {"name":"七贤巷","start_id":18,"end_id":19,"limit_speed":6.94,"degree":3},
    {"name":"八道沟","start_id":19,"end_id":20,"limit_speed":6.94,"degree":3},
    {"name":"九中街","start_id":20,"end_id":21,"limit_speed":6.94,"degree":3},
    {"name":"园通路","start_id":20,"end_id":25,"limit_speed":6.94,"degree":3},
    {"name":"东头巷","start_id":16,"end_id":22,"limit_speed":6.94,"degree":3},
    {"name":"南坡路","start_id":22,"end_id":23,"limit_speed":6.94,"degree":3},
    {"name":"北关街","start_id":23,"end_id":24,"limit_speed":6.94,"degree":3},
    {"name":"致富路","start_id":23,"end_id":28,"limit_speed":6.94,"degree":3},
    {"name":"前街","start_id":24,"end_id":25,"limit_speed":6.94,"degree":3},
    {"name":"南丰巷","start_id":25,"end_id":30,"limit_speed":6.94,"degree":3},
    {"name":"西巷口","start_id":26,"end_id":27,"limit_speed":6.94,"degree":3},
    {"name":"平安巷","start_id":27,"end_id":28,"limit_speed":6.94,"degree":3},
    {"name":"拥军街","start_id":28,"end_id":29,"limit_speed":6.94,"degree":3},
    {"name":"港边路","start_id":29,"end_id":30,"limit_speed":6.94,"degree":3},
    {"name":"东兴路","start_id":24,"end_id":29,"limit_speed":6.94,"degree":3},
    {"name":"西平街","start_id":17,"end_id":24,"limit_speed":6.94,"degree":3},
    {"name":"向阳路","start_id":22,"end_id":26,"limit_speed":6.94,"degree":3},
    {"name":"北顺道","start_id":18,"end_id":25,"limit_speed":6.94,"degree":3},
    {"name":"市心路","start_id":30,"end_id":21,"limit_speed":6.94,"degree":3}
]

# ===================== 选取路线 =====================
# 路线：松风涧(0) → 云岫台(2) → 花溪渡(3) → 荷风榭(9)
path_ids = [0, 2, 3, 9]
path_xy = np.array([[points[i]['x'], points[i]['y']] for i in path_ids])

# 生成平滑路径
def interp_path(path, num=200):
    t = np.linspace(0, len(path)-1, num)
    x = np.interp(t, np.arange(len(path)), path[:,0])
    y = np.interp(t, np.arange(len(path)), path[:,1])
    return np.column_stack([x, y])

path_smooth = interp_path(path_xy, num=300)
n_frames = len(path_smooth)

# 车队参数：5辆车，编队间距
car_num = 5
follow_dist = 15  # 帧间隔，越大车距越远
cars_x = np.zeros((car_num, n_frames))
cars_y = np.zeros((car_num, n_frames))

for i in range(car_num):
    shift = max(0, i * follow_dist)
    cars_x[i] = np.roll(path_smooth[:,0], shift)
    cars_y[i] = np.roll(path_smooth[:,1], shift)
    # 开头补起点
    cars_x[i,:shift] = path_smooth[0,0]
    cars_y[i,:shift] = path_smooth[0,1]

# ===================== 绘图初始化 =====================
fig, ax = plt.subplots(figsize=(12,10), dpi=100)

# 画道路
for edge in edges:
    s = points[edge['start_id']]
    e = points[edge['end_id']]
    ax.plot([s['x'],e['x']], [s['y'],e['y']], c='#777', lw=1.2, alpha=0.7)

# 画点位
ax.scatter([p['x']for p in points], [p['y']for p in points],
           c='#409eff', s=40, zorder=3)

# 画选中路线
ax.plot(path_xy[:,0], path_xy[:,1], c='crimson', lw=3, alpha=0.6, label='编队路线')

# 车队车辆
colors = ['red','orange','green','blue','purple']
cars = [ax.plot([],[],'o',ms=10,c=colors[i],zorder=5)[0] for i in range(car_num)]

ax.set_title('多车编队行驶动画', fontsize=16)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.axis('equal')
ax.grid(alpha=0.3)
ax.legend()

# ===================== 动画更新函数 =====================
def update(frame):
    for i in range(car_num):
        cars[i].set_data(cars_x[i,frame], cars_y[i,frame])
    return cars

# ===================== 生成GIF =====================
ani = FuncAnimation(
    fig, update, frames=n_frames,
    interval=50, blit=True
)

# 保存动图
ani.save('fleet_animation.gif', writer='pillow', dpi=100)
plt.show()