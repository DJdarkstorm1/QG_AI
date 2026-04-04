import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# 读取文件车辆初始状态与邻接矩阵(通信拓补图)
f = open("./input.json","r",encoding="utf-8")
# print(type(f))
raw_data = json.load(f)
f.close()
print(raw_data)
# 选择第i-1个数据
# 0 是情况1的数据
# 1 是情况2
SELECT = 0

CARS_NUM = raw_data[SELECT]["cars_num"]
CARS = raw_data[SELECT]["cars"]
MATRIX_A = raw_data[SELECT]["A"]
MATRIX_K = raw_data[SELECT]["K"]

# ============== 自适应检测参数 ==============
ENABLE_ADAPTIVE = True           # 是否启用自适应结束
POS_THRESHOLD = 0.1              # 位置误差阈值（米）
VEL_THRESHOLD = 0.05             # 速度误差阈值（米/秒）
STABLE_TIME = 2.0                # 需要稳定持续的时间（秒）
MIN_SIM_TIME = 5.0               # 最小仿真时间（秒）
# ===========================================

# 1.初始参数

cars_num = CARS_NUM
total_time = 30
dt = 0.1
steps = int(total_time/dt)
Leader_id = 0 # 设置默认为第一个
# 初始位置          x, y 速度 vx,vy 期望间距 x,y
POS_X = 0 # x坐标索引
POS_Y = 1 # y坐标索引
VEC_X = 2 # x速度索引
VEC_Y = 3 # y速度索引
AIM_X = 4 # 目标x坐标
AIM_Y = 5 # 目标y坐标
cars = np.array(CARS)

# 通信拓补邻接矩阵
A = np.array(MATRIX_A)

# 链接矩阵K:与Leader链接的
K = np.array(MATRIX_K)

# 度矩阵和拉普拉斯矩阵
D = np.diag(np.sum(A, axis=1))
L = D - A

leader_speed_x = np.zeros(steps)
leader_speed_y = np.zeros(steps)
# Leader匀速：记录下Leader速度
for t in range(steps):
    leader_speed_x[t] = cars[Leader_id][VEC_X]
    leader_speed_y[t] = cars[Leader_id][VEC_Y]

# print(leader_speed)
leader_position_x = np.zeros(steps)
leader_position_y = np.zeros(steps)
# 设置Leader初始位置
leader_position_x[Leader_id] = cars[Leader_id][POS_X] # 初始x位置
leader_position_y[Leader_id] = cars[Leader_id][POS_Y] # 初始y位置

for t in range(1, steps):
    leader_position_x[t] = (leader_position_x[t - 1]
                            + leader_speed_x[t - 1] * dt)
    leader_position_y[t] = (leader_position_y[t - 1]
                            + leader_speed_y[t - 1] * dt)
# 储存初始状态
states = np.zeros((cars_num, steps, 6))
for i in range(cars_num):
   states[i, 0] = cars[i]

# 控制参数
beta = 2.0
gamma = 1.0

# 2.计算
# 计算相对位置
r_i_j = np.zeros((cars_num, cars_num, 2))

for i in range(cars_num):
    for j in range(cars_num):
        if i != j:
            if j==0:# Leader
                r_i_j[i, j] = [cars[i][AIM_X], cars[j][AIM_X]]
            else:
                r_i_j[i, j] = [cars[i][AIM_X] - cars[j][AIM_X],
                               cars[i][AIM_Y] - cars[j][AIM_Y]]

# ============== 自适应检测变量 ==============
if ENABLE_ADAPTIVE:
    stable_counter = 0                      # 连续稳定步数计数器
    stable_steps_needed = int(STABLE_TIME / dt)  # 需要的连续稳定步数
    min_steps = int(MIN_SIM_TIME / dt)      # 最小仿真步数
    completion_step = None                  # 完成时的步数
    print(f"自适应检测已启用")
    print(f"  - 位置阈值: {POS_THRESHOLD}m")
    print(f"  - 速度阈值: {VEL_THRESHOLD}m/s")
    print(f"  - 需要稳定时间: {STABLE_TIME}s ({stable_steps_needed}步)")
    print(f"  - 最小仿真时间: {MIN_SIM_TIME}s ({min_steps}步)")
    print("-" * 50)
# ==========================================

print("仿真开始...")

for t in range(1, steps):
    # 更新Leader
    states[Leader_id, t,POS_X] = leader_position_x[t]
    states[Leader_id, t,POS_Y] = leader_position_y[t]
    states[Leader_id, t,VEC_X] = leader_speed_x[t]
    states[Leader_id, t,VEC_Y] = leader_speed_y[t]

    # 更新follower
    for i in range (1, cars_num):
        # 保存当前状态
        pos_i = np.array([states[i, t - 1, POS_X], states[i, t - 1, POS_Y]])
        vec_i = np.array([states[i, t - 1, VEC_X], states[i, t - 1, VEC_Y]])

        # 与邻接车交互的项(1)
        neighbor_term = np.zeros(2)
        neighbors = np.where(A[i] > 0)[0] # 找到邻接车

        effective_neighbors = []
        for j in neighbors:
            if A[i][j] == 1:
                effective_neighbors.append(j)
        # print("+++++++", effective_neighbors)
        if len(effective_neighbors) > 0:
            for j in effective_neighbors:
                pos_j = np.array([states[j, t - 1, POS_X], states[j, t - 1, POS_Y]])
                vec_j = np.array([states[j, t - 1, VEC_X], states[j, t - 1, VEC_Y]])

                # 位置误差
                pos_error = (pos_i - pos_j) - r_i_j[i, j]
                # 速度误差
                vec_error = vec_i - vec_j

                neighbor_term += A[i, j] * (pos_error + beta * vec_error)
        # 与Leader交互的项(2)
        leader_term = np.zeros(2)
        if K[i] > 0:
            pos_L = np.array([states[Leader_id, t - 1, POS_X], states[Leader_id, t - 1, POS_Y]])
            vec_L = np.array([states[Leader_id, t - 1, VEC_X], states[Leader_id, t - 1, VEC_Y]])

            r_i = np.array([cars[i][AIM_X], cars[i][AIM_Y]])

            pos_error_L = (pos_i - pos_L) - r_i
            vec_error_L = vec_i - vec_L

            leader_term = K[i] * (pos_error_L + gamma * vec_error_L)

        # 控制输入
        u_i = -neighbor_term - leader_term

        # 更新状态
        states[i, t, POS_X] = states[i, t - 1, POS_X] + states[i, t - 1, VEC_X] * dt
        states[i, t, POS_Y] = states[i, t - 1, POS_Y] + states[i, t - 1, VEC_Y] * dt
        states[i, t, VEC_X] = states[i, t - 1, VEC_X] + u_i[0] * dt
        states[i, t, VEC_Y] = states[i, t - 1, VEC_Y] + u_i[1] * dt

        # 目标位置不变
        states[i, t, AIM_X] = states[i, t - 1, AIM_X]
        states[i, t, AIM_Y] = states[i, t - 1, AIM_Y]

    # 自适应检测:10s后检测
    current_time = t * dt
    # ============== 自适应检测（改进版） ==============
    if ENABLE_ADAPTIVE and t >= min_steps:
        # 计算当前所有车辆的最大误差
        max_pos_error = 0
        max_vel_error = 0

        for i in range(1, cars_num):
            # 纵向位置误差
            lon_error = abs(states[i, t, POS_X] - states[Leader_id, t, POS_X] - cars[i][AIM_X])
            # 横向位置误差
            lat_error = abs(states[i, t, POS_Y] - states[Leader_id, t, POS_Y] - cars[i][AIM_Y])
            # 速度误差（欧氏距离）
            vel_error = np.sqrt((states[i, t, VEC_X] - states[Leader_id, t, VEC_X]) ** 2 +
                                (states[i, t, VEC_Y] - states[Leader_id, t, VEC_Y]) ** 2)

            max_pos_error = max(max_pos_error, lon_error, lat_error)
            max_vel_error = max(max_vel_error, vel_error)

        # 判断是否满足阈值
        if max_pos_error < POS_THRESHOLD and max_vel_error < VEL_THRESHOLD:
            stable_counter += 1
            # 达到稳定持续时间要求
            if stable_counter >= stable_steps_needed:
                completion_step = t
                completion_time = current_time - STABLE_TIME + dt
                print(f"\n✓ 编队检测完成！")
                print(f"  完成时间: {completion_time:.2f} 秒")
                print(f"  完成步数: {completion_step}")
                print(f"  最大位置误差: {max_pos_error:.3f} m")
                print(f"  最大速度误差: {max_vel_error:.3f} m/s")
                break
        else:
            stable_counter = 0  # 重置计数器
    # =============================================

# 截断状态数组（如果提前结束）
if ENABLE_ADAPTIVE and completion_step is not None and completion_step < steps - 1:
    states = states[:, :completion_step + 1, :]
    steps = completion_step + 1
    print(f"仿真提前结束，实际时长: {steps * dt:.2f} 秒")
else:
    print(f"仿真完成，时长: {steps * dt:.2f} 秒")


print("仿真完成")

# print(states[0][-5:])
# print(states[1][-5:])
# ---------------------- 可视化 ----------------
plt.figure(figsize=(18, 12))

labels = []
for i in range(cars_num):
    if i == Leader_id:
        labels.append("Leader")
    else:
        labels.append("Vehicle {}".format(i))
time_array = np.arange(steps) * dt
print(time_array.shape)
# 图1: X-Y位置关系图
ax1 = plt.subplot(2, 3, 1)
for i in range(cars_num):
    ax1.plot(states[i, :, POS_X], states[i, :, POS_Y],
            label=labels[i], linewidth=2)
# 标记起点和终点
for i in range(cars_num):
    # 起点
    ax1.scatter(states[i, 0, POS_X], states[i, 0, POS_Y],
                s=100, marker='o', edgecolors='black', zorder=5)
    # 4s
    ax1.scatter(states[i, 40, POS_X], states[i, 40, POS_Y],
                s=100, marker='>', edgecolors='black', zorder=5)

    # 10s
    ax1.scatter(states[i, 100, POS_X], states[i, 100, POS_Y],
                s=100, marker='>', edgecolors='black', zorder=5)
    # # 20s
    # ax1.scatter(states[i, 200, POS_X], states[i, 200, POS_Y],
    #             s=100, marker='>', edgecolors='black', zorder=5)

    # 终点
    ax1.scatter(states[i, -1, POS_X], states[i, -1, POS_Y],
                s=100, marker='>', edgecolors='black', zorder=5)

ax1.set_xlabel('X Position (m)')
ax1.set_ylabel('Y Position (m)')
# ax1.set_xlim(0, 160)
# ax1.set_ylim(0, 80)
ax1.legend()
ax1.tick_params(direction="in",top=True, right=True, color='black', axis='both',
               labelcolor='black')

# t-Longtitudinal Gap(m)
ax2 = plt.subplot(2, 3, 2)
for i in range(cars_num):
    longitudinal_gap = states[i, :, POS_X] - states[Leader_id, :, POS_X]
    ax2.plot(time_array, longitudinal_gap,
             label=labels[i], linewidth=2)
    desired_gap = cars[i][AIM_X]
    ax2.axhline(y=desired_gap, linestyle='--',
                alpha=0.5, linewidth=1)
# 标记断联点

ax2.set_xlabel('时间 (秒)')
ax2.set_ylabel('纵向间距 (米)')

# ax2.set_xlim(0, 10)
# ax2.set_ylim(-25, 5)
ax2.legend()

# 图3: 时间与横向间距
ax3 = plt.subplot(2, 3, 3)
for i in range(cars_num):
    lateral_gap = states[i, :, POS_Y] - states[Leader_id, :, POS_Y]
    ax3.plot(time_array[:150], lateral_gap[:150],
             label=labels[i], linewidth=2)

ax3.set_xlabel('时间 (秒)')
ax3.set_ylabel('横向间距 (米)')
# ax3.set_xlim(0, 15)
# ax3.set_ylim(-10, 20)
ax3.legend()

# 图4: 时间与纵向速度 V_x
ax4 = plt.subplot(2, 3, 4)
for i in range(cars_num):
    ax4.plot(time_array, states[i, :, VEC_X],
             label=labels[i], linewidth=2)

ax4.set_xlabel('时间 (秒)')
ax4.set_ylabel('纵向速度 Vx (m/s)')
# ax4.set_xlim(0, 15)
# ax4.set_ylim(-10, 10)
ax4.legend()

# 图5: 时间与横向速度 V_y
ax5 = plt.subplot(2, 3, 5)
for i in range(cars_num):
    ax5.plot(time_array, states[i, :, VEC_Y],
             label=labels[i], linewidth=2)
ax5.set_xlabel('时间 (秒)')
ax5.set_ylabel('横向速度 Vy (m/s)')
# ax5.set_xlim(0, 15)
# ax5.set_ylim(-10, 10)
ax5.legend()

# 图6: 通信拓扑图
ax6 = plt.subplot(2, 3, 6)

node_pos = {}
node_labels = {}
for i in range(cars_num):
    if i == Leader_id:
        node_labels.update({i:'Leader'})
    else:
        node_labels.update({i:'车{}'.format(i)})
    if i%2 == 0:
        node_pos.update({i: (i, 0)})
    else:
        node_pos.update({i: (i-1, 1)})

    circle = plt.Circle(node_pos[i], 0.2,
                        edgecolor="black", linewidth=1, alpha=0.7)
    ax6.add_patch(circle)
    ax6.text(node_pos[i][0], node_pos[i][1], node_labels[i],
             ha='center', va='center', fontsize=10, fontweight='bold')

for i in range(cars_num):
    for j in range(cars_num):
        if A[i, j] > 0:
            linestyle = '-'
            color = 'black'
            alpha = 0.8

            ax6.annotate('', xy=(node_pos[i][0], node_pos[i][1]),
                         xytext=(node_pos[j][0], node_pos[j][1]),
                         arrowprops=dict(arrowstyle='->', lw=1.5,
                                         alpha=alpha,
                                         linestyle=linestyle))

ax6.set_xlim(-1, cars_num)
ax6.set_ylim(-0.2, 1.3)


ax6.axis('off')

plt.tight_layout()
plt.show()
