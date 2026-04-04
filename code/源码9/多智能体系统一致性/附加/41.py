import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random
import math
import os

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# ========== 加载地图数据 ==========
f = open("./data.json", "r", encoding="utf-8")
raw_data = json.load(f)
f.close()

point_list = raw_data["points"]
edge_list = raw_data["edges"]

df_point = pd.DataFrame(point_list)
df_edge = pd.DataFrame(edge_list)

print(f"加载完成: {len(point_list)} 个点, {len(edge_list)} 条边")


# ========== 找到所有连续3段道路的路径 ==========
def find_all_continuous_paths(edge_list, point_list):
    """找到所有连续3段道路的路径，返回路径的边序列和节点序列"""
    adj = {}
    for edge in edge_list:
        s, e = edge['start_id'], edge['end_id']
        if s not in adj:
            adj[s] = []
        if e not in adj:
            adj[e] = []
        adj[s].append((e, edge))
        adj[e].append((s, edge))

    valid_paths = []

    for start_edge in edge_list:
        for start_node in [start_edge['start_id'], start_edge['end_id']]:
            def dfs(node, visited_edges, visited_nodes, depth):
                if depth == 3:
                    return visited_edges[:], visited_nodes[:]

                for neighbor, edge in adj.get(node, []):
                    if edge not in visited_edges:
                        visited_edges.append(edge)
                        visited_nodes.append(neighbor)
                        result = dfs(neighbor, visited_edges, visited_nodes, depth + 1)
                        if result:
                            return result
                        visited_edges.pop()
                        visited_nodes.pop()
                return None

            result = dfs(start_node, [start_edge], [start_node], 1)
            if result:
                edges, nodes = result
                if len(edges) == 3:
                    valid_paths.append((edges, nodes))

    unique_paths = []
    for path in valid_paths:
        edges = path[0]
        edge_names = tuple(sorted([e['name'] for e in edges]))
        if edge_names not in [tuple(sorted([e['name'] for e in p[0]])) for p in unique_paths]:
            unique_paths.append(path)

    return unique_paths


all_paths = find_all_continuous_paths(edge_list, point_list)
print(f"找到 {len(all_paths)} 条连续3段道路")

if len(all_paths) == 0:
    print("未找到连续3段道路，使用前3条边")
    selected_edges = edge_list[:3]
    nodes = [selected_edges[0]['start_id'], selected_edges[0]['end_id']]
    for edge in selected_edges[1:]:
        if edge['start_id'] == nodes[-1]:
            nodes.append(edge['end_id'])
        elif edge['end_id'] == nodes[-1]:
            nodes.append(edge['start_id'])
        else:
            nodes.append(edge['start_id'])
            nodes.append(edge['end_id'])
else:
    selected_edges, nodes = random.choice(all_paths)

print(f"选中的道路: {[e['name'] for e in selected_edges]}")
print(f"节点序列: {[point_list[n]['name'] for n in nodes]}")

route_start_node = nodes[0]
route_start_point = point_list[route_start_node]
route_end_node = nodes[-1]
route_end_point = point_list[route_end_node]

print(f"\n路线起点: {route_start_point['name']} (ID: {route_start_node})")
print(f"路线终点: {route_end_point['name']} (ID: {route_end_node})")

# ========== 构建完整路径点序列 ==========
path_points = []
path_nodes = []

for node_id in nodes:
    point = point_list[node_id]
    path_points.append([point['x'], point['y']])
    path_nodes.append(node_id)

path_points = np.array(path_points)


# ========== 路径参数计算 ==========
def calculate_path_length(points):
    if len(points) < 2:
        return 0
    total = 0
    for i in range(len(points) - 1):
        total += np.linalg.norm(points[i + 1] - points[i])
    return total


def get_position_on_path(points, s):
    if len(points) < 2:
        return points[0], np.array([1, 0])

    total_len = calculate_path_length(points)
    if s >= total_len:
        if len(points) >= 2:
            last_dir = points[-1] - points[-2]
            if np.linalg.norm(last_dir) > 0:
                last_dir = last_dir / np.linalg.norm(last_dir)
            else:
                last_dir = np.array([1, 0])
            return points[-1], last_dir
        return points[-1], np.array([1, 0])

    current_dist = 0
    for i in range(len(points) - 1):
        seg_vec = points[i + 1] - points[i]
        seg_len = np.linalg.norm(seg_vec)

        if current_dist + seg_len >= s:
            ratio = (s - current_dist) / seg_len
            pos = points[i] + seg_vec * ratio
            direction = seg_vec / seg_len
            return pos, direction

        current_dist += seg_len

    return points[-1], np.array([1, 0])


path_length = calculate_path_length(path_points)
print(f"路径总长度: {path_length:.2f}m")

# ========== 车辆参数 ==========
cars_num = 4
total_time = max(30, min(60, path_length / 5 + 10))
dt = 0.05
steps = int(total_time / dt)
Leader_id = 0

initial_offsets = [0, -8, -16, -24]

cars = np.zeros((cars_num, 6))
for i in range(cars_num):
    offset = max(0, initial_offsets[i])
    pos, direction = get_position_on_path(path_points, offset)
    cars[i] = [pos[0], pos[1], 6 + i * 0.5, 0, 0, 0]

A = np.array([[0, 1, 1, 0],
              [1, 0, 1, 1],
              [1, 1, 0, 1],
              [0, 1, 1, 0]])

K = np.array([0, 1, 1, 0])

states = np.zeros((cars_num, steps, 6))
for i in range(cars_num):
    states[i, 0] = cars[i]

beta, gamma = 1.0, 1.0
desired_gap = 8

r_i = np.array([[0, 0], [-desired_gap, 0], [-2 * desired_gap, 0], [-3 * desired_gap, 0]])

r_ij = np.zeros((cars_num, cars_num, 2))
for i in range(cars_num):
    for j in range(cars_num):
        if i != j:
            r_ij[i, j] = r_i[i] - r_i[j]

leader_arc_lengths = np.zeros(steps)

print("开始仿真...")
leader_speed = 6.0

for t in range(1, steps):
    leader_arc = leader_speed * t * dt
    if leader_arc > path_length:
        leader_arc = path_length

    leader_arc_lengths[t] = leader_arc
    leader_pos, leader_dir = get_position_on_path(path_points, leader_arc)

    states[0, t, 0:2] = leader_pos
    states[0, t, 2:4] = [leader_speed * leader_dir[0], leader_speed * leader_dir[1]]

    for i in range(1, cars_num):
        pos_i = states[i, t - 1, 0:2]
        vec_i = states[i, t - 1, 2:4]

        expected_pos = leader_pos - leader_dir * (desired_gap * i)
        pos_error = (pos_i - expected_pos)
        vel_error = vec_i - states[0, t, 2:4]

        neighbor_term = np.zeros(2)
        neighbors = np.where(A[i] > 0)[0]

        for j in neighbors:
            if j == 0:
                continue
            if j < cars_num:
                pos_j = states[j, t - 1, 0:2]
                vec_j = states[j, t - 1, 2:4]
                neighbor_term += A[i, j] * ((pos_i - pos_j - r_ij[i, j]) + beta * (vec_i - vec_j))

        leader_term = np.zeros(2)
        if K[i] > 0:
            leader_term = K[i] * (pos_error + gamma * vel_error)

        u_i = -neighbor_term - leader_term
        u_i = np.clip(u_i, -5, 5)

        states[i, t, 0:2] = states[i, t - 1, 0:2] + states[i, t - 1, 2:4] * dt
        states[i, t, 2:4] = states[i, t - 1, 2:4] + u_i * dt
        states[i, t, 2:4] = np.clip(states[i, t, 2:4], 0, 12)

print("仿真完成！")

# ========== 可视化1: 全局地图 ==========
fig1 = plt.figure(figsize=(14, 12))
ax1 = fig1.add_subplot(111)

for edge in edge_list:
    start = point_list[edge["start_id"]]
    end = point_list[edge["end_id"]]
    ax1.plot([start["x"], end["x"]], [start["y"], end["y"]],
             color="#DDDDDD", linewidth=1.5, alpha=0.5, zorder=1)

for i, edge in enumerate(selected_edges):
    start = point_list[edge["start_id"]]
    end = point_list[edge["end_id"]]
    ax1.plot([start["x"], end["x"]], [start["y"], end["y"]],
             color="#FF3333", linewidth=6, alpha=0.9, zorder=3)

ax1.scatter(df_point["x"], df_point["y"], color="#AAAAAA", s=40, zorder=2, alpha=0.6)

for i, node_id in enumerate(path_nodes):
    point = point_list[node_id]
    if i == 0:
        color = '#00AA00'
        size = 280
    elif i == len(path_nodes) - 1:
        color = '#FF6600'
        size = 280
    else:
        color = '#FF8888'
        size = 120
    ax1.scatter(point['x'], point['y'], color=color, s=size, marker='o',
                zorder=4, edgecolors='black', linewidth=1.5)

for i, node_id in enumerate(path_nodes):
    point = point_list[node_id]
    offset_y = 35 if i == 0 or i == len(path_nodes) - 1 else 25
    ax1.text(point['x'], point['y'] + offset_y, point['name'],
             fontsize=10, ha='center', fontweight='bold', color='black')

ax1.scatter(route_start_point['x'], route_start_point['y'], color='green', s=350,
            marker='*', zorder=5, edgecolors='black', linewidth=2, label='起点')
ax1.scatter(route_end_point['x'], route_end_point['y'], color='orange', s=350,
            marker='*', zorder=5, edgecolors='black', linewidth=2, label='终点')

ax1.set_title("行驶路线地图", fontsize=16, pad=20)
ax1.set_xlabel("X 坐标 (m)", fontsize=12)
ax1.set_ylabel("Y 坐标 (m)", fontsize=12)
ax1.grid(True, alpha=0.2)
ax1.set_xlim([0, 6500])
ax1.set_ylim([0, 6500])
ax1.legend(loc='upper right')
plt.tight_layout()
plt.savefig('global_map_route.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== 可视化2: 行驶路线详细2D图 ==========
fig2 = plt.figure(figsize=(14, 8))
ax2 = fig2.add_subplot(111)

for i in range(len(path_points) - 1):
    ax2.plot([path_points[i][0], path_points[i + 1][0]],
             [path_points[i][1], path_points[i + 1][1]],
             color='#FF3333', linewidth=8, alpha=0.8, zorder=1)

for i, (x, y) in enumerate(path_points):
    if i == 0:
        color = 'green'
        size = 280
    elif i == len(path_points) - 1:
        color = 'orange'
        size = 280
    else:
        color = '#FF8888'
        size = 150
    ax2.scatter(x, y, color=color, s=size, zorder=4, edgecolors='black', linewidth=2)

for i, (x, y) in enumerate(path_points):
    node = point_list[path_nodes[i]]
    offset_y = 35 if i == 0 or i == len(path_points) - 1 else 25
    ax2.text(x, y + offset_y, node['name'], fontsize=11, ha='center', fontweight='bold')

for i, edge in enumerate(selected_edges):
    start = point_list[edge["start_id"]]
    end = point_list[edge["end_id"]]
    mid_x = (start["x"] + end["x"]) / 2
    mid_y = (start["y"] + end["y"]) / 2
    ax2.text(mid_x, mid_y - 50, edge['name'], fontsize=11, ha='center', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

ax2.set_title(f"行驶路线: {selected_edges[0]['name']} → {selected_edges[1]['name']} → {selected_edges[2]['name']}",
              fontsize=14)
ax2.set_xlabel("X 坐标 (m)", fontsize=12)
ax2.set_ylabel("Y 坐标 (m)", fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.axis('equal')
plt.tight_layout()
plt.savefig('route_detailed.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== 可视化3: 3D道路和车辆动画（修复GIF保存问题）==========
print("\n正在生成3D动画...")

# 减少帧数，避免量化错误
frame_count = int(min(total_time * 5, 300))  # 限制最大帧数
frame_step = max(1, steps // frame_count)

fig3 = plt.figure(figsize=(16, 10))
ax3 = fig3.add_subplot(111, projection='3d')

colors = ['#FF3333', '#33FF33', '#3399FF', '#FF9933']
labels = ['Leader', 'Vehicle 2', 'Vehicle 3', 'Vehicle 4']

ax3.set_xlabel('X (m)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Y (m)', fontsize=12, fontweight='bold')
ax3.set_zlabel('Z (m)', fontsize=12, fontweight='bold')
ax3.set_title('车队沿行驶路线行驶 (3D视图)', fontsize=14, fontweight='bold')
ax3.view_init(elev=35, azim=-45)

x_min, x_max = path_points[:, 0].min() - 100, path_points[:, 0].max() + 100
y_min, y_max = path_points[:, 1].min() - 100, path_points[:, 1].max() + 100
ax3.set_xlim(x_min, x_max)
ax3.set_ylim(y_min, y_max)
ax3.set_zlim(0, 3)

# 绘制3D行驶路线
for i in range(len(path_points) - 1):
    ax3.plot([path_points[i][0], path_points[i + 1][0]],
             [path_points[i][1], path_points[i + 1][1]],
             [0, 0], color='#FF3333', linewidth=8, alpha=0.8, zorder=1)

for i, (x, y) in enumerate(path_points):
    color = 'green' if i == 0 else ('orange' if i == len(path_points) - 1 else '#FF8888')
    size = 120 if i == 0 or i == len(path_points) - 1 else 80
    ax3.scatter(x, y, 0, color=color, s=size, zorder=2, edgecolors='black')


class Vehicle3D:
    def __init__(self, ax, color):
        self.ax = ax
        self.color = color
        self.body = None

    def create(self, x, y, z, direction, speed):
        length, width, height = 2.5, 1.6, 0.5
        angle = math.atan2(direction[1], direction[0])
        cos_a, sin_a = math.cos(angle), math.sin(angle)

        vertices = []
        for dx in [-length / 2, length / 2]:
            for dy in [-width / 2, width / 2]:
                rx = dx * cos_a - dy * sin_a
                ry = dx * sin_a + dy * cos_a
                for dz in [0, height]:
                    vertices.append([x + rx, y + ry, z + dz])

        faces_idx = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
        body_vertices = [[vertices[idx] for idx in face] for face in faces_idx]

        alpha = min(0.6 + speed * 0.05, 0.9)
        if self.body:
            self.body.remove()
        self.body = Poly3DCollection(body_vertices, alpha=alpha,
                                     facecolor=self.color, edgecolor='black', linewidth=1)
        self.ax.add_collection3d(self.body)


vehicles = [Vehicle3D(ax3, colors[i]) for i in range(cars_num)]

comm_lines = []
time_text = ax3.text2D(0.02, 0.95, '', transform=ax3.transAxes, fontsize=12,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
status_text = ax3.text2D(0.02, 0.88, '', transform=ax3.transAxes, fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))


def update_animation(frame_idx):
    t = frame_idx * frame_step * dt
    idx = min(frame_idx * frame_step, steps - 1)

    for i in range(cars_num):
        pos = states[i, idx, 0:2]
        vel = states[i, idx, 2:4]
        speed = np.linalg.norm(vel)
        direction = vel / speed if speed > 0.1 else np.array([1, 0])
        vehicles[i].create(pos[0], pos[1], 0, direction, speed)

    for line in comm_lines:
        if line:
            try:
                line.remove()
            except:
                pass
    comm_lines.clear()

    for i in range(cars_num):
        for j in range(cars_num):
            if A[i, j] > 0 and i != j:
                x1, y1 = states[i, idx, 0], states[i, idx, 1]
                x2, y2 = states[j, idx, 0], states[j, idx, 1]
                line = ax3.plot([x1, x2], [y1, y2], [0.6, 0.6],
                                color='cyan', linewidth=2, alpha=0.6, linestyle='--')
                comm_lines.extend(line)

    time_text.set_text(f'时间: {t:.1f}s')
    progress = leader_arc_lengths[idx] / path_length * 100
    status_text.set_text(f'进度: {progress:.1f}%')

    return vehicles + comm_lines + [time_text, status_text]


frames = range(0, frame_count)
anim = FuncAnimation(fig3, update_animation, frames=frames,
                     interval=50, blit=False, repeat=False)

# 尝试多种方式保存GIF
gif_saved = False

# 方法1: 使用PillowWriter（降低质量和帧率）
try:
    print("尝试使用PillowWriter保存GIF...")
    writer = PillowWriter(fps=10, bitrate=500, dpi=80)
    anim.save('route_3d_animation.gif', writer=writer, dpi=80)
    print("3D动画已保存为: route_3d_animation.gif")
    gif_saved = True
except Exception as e:
    print(f"PillowWriter保存失败: {e}")

# 方法2: 保存为MP4（如果安装了ffmpeg）
if not gif_saved:
    try:
        print("尝试保存为MP4格式...")
        anim.save('route_3d_animation.mp4', writer='ffmpeg', fps=10)
        print("3D动画已保存为: route_3d_animation.mp4")
        gif_saved = True
    except Exception as e:
        print(f"MP4保存失败: {e}")

# 方法3: 保存为HTML文件
if not gif_saved:
    try:
        print("尝试保存为HTML文件...")
        from matplotlib.animation import HTMLWriter

        writer = HTMLWriter(fps=10)
        anim.save('route_3d_animation.html', writer=writer)
        print("3D动画已保存为: route_3d_animation.html")
        gif_saved = True
    except Exception as e:
        print(f"HTML保存失败: {e}")

plt.show()

# ========== 可视化4: 2D实时位置动画 ==========
print("\n生成2D位置动画...")

fig4 = plt.figure(figsize=(14, 10))
ax4 = fig4.add_subplot(111)

for i in range(len(path_points) - 1):
    ax4.plot([path_points[i][0], path_points[i + 1][0]],
             [path_points[i][1], path_points[i + 1][1]],
             color='#FF3333', linewidth=8, alpha=0.6, zorder=1)

ax4.scatter(path_points[:, 0], path_points[:, 1], color='red', s=150, zorder=2)

vehicle_scatters = []
for i in range(cars_num):
    scatter = ax4.scatter([], [], s=200, c=colors[i], marker='s',
                          edgecolors='black', linewidth=2, label=labels[i], zorder=10)
    vehicle_scatters.append(scatter)

comm_lines_2d = []

ax4.set_xlim(x_min, x_max)
ax4.set_ylim(y_min, y_max)
ax4.set_xlabel('X 坐标 (m)', fontsize=12)
ax4.set_ylabel('Y 坐标 (m)', fontsize=12)
ax4.set_title(f'车辆实时运动位置', fontsize=14)
ax4.grid(True, alpha=0.3)
ax4.legend(loc='upper right')

time_text_2d = ax4.text(0.02, 0.95, '', transform=ax4.transAxes, fontsize=12,
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))


def update_2d(frame_idx):
    t = frame_idx * frame_step * dt
    idx = min(frame_idx * frame_step, steps - 1)

    for i in range(cars_num):
        vehicle_scatters[i].set_offsets([[states[i, idx, 0], states[i, idx, 1]]])

    for line in comm_lines_2d:
        if line:
            try:
                line.remove()
            except:
                pass
    comm_lines_2d.clear()

    for i in range(cars_num):
        for j in range(cars_num):
            if A[i, j] > 0 and i != j:
                line = ax4.plot([states[i, idx, 0], states[j, idx, 0]],
                                [states[i, idx, 1], states[j, idx, 1]],
                                color='cyan', linewidth=2, alpha=0.6, linestyle='--')
                comm_lines_2d.extend(line)

    time_text_2d.set_text(f'时间: {t:.1f}s')
    return vehicle_scatters + comm_lines_2d + [time_text_2d]


frames = range(0, frame_count)
anim2 = FuncAnimation(fig4, update_2d, frames=frames,
                      interval=50, blit=False, repeat=False)

try:
    writer2 = PillowWriter(fps=10, bitrate=500, dpi=80)
    anim2.save('route_2d_position.gif', writer=writer2, dpi=80)
    print("2D位置动画已保存为: route_2d_position.gif")
except Exception as e:
    print(f"2D动画保存失败: {e}")
    try:
        anim2.save('route_2d_position.mp4', writer='ffmpeg', fps=10)
        print("2D动画已保存为: route_2d_position.mp4")
    except:
        pass

plt.show()

print("\n" + "=" * 60)
print("仿真完成！")
print(f"行驶路线: {[e['name'] for e in selected_edges]}")
print(f"路线起点: {route_start_point['name']}")
print(f"路线终点: {route_end_point['name']}")
print(f"路径总长度: {path_length:.2f}m")
print("\n生成的文件:")
print("1. global_map_route.png - 全局地图")
print("2. route_detailed.png - 行驶路线详细图")
print("3. route_3d_animation.gif/mp4/html - 3D行驶动画")
print("4. route_2d_position.gif/mp4 - 2D位置动画")
print("=" * 60)