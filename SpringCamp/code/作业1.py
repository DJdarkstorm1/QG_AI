import json
import numpy as np
from MyCoordinate import CoordinateConvert

'''
# 验算
old_vector = np.array([1,1])
old_axis = np.array([[1,0],[0,1]])
new_axis = np.array([[1,0],[1,1]])
new_vector = cv.change_axis(old_vector, old_axis, new_axis)
print(new_vector)
#print(axis_angle(old_vector, new_axis))

print(cv.axis_projection(new_vector, old_axis)) # 要新的向量在原来的坐标系下求投影长度才正确
'''

cv = CoordinateConvert()

f = open("./data(1).json","r",encoding="utf-8")
data = json.load(f)
f.close()
print(type(data))
obj_dict_list = []


for group in data:

    dict_obj = {}
    obj_list = [] # 保存目标坐标系的列表
    area_list = [] # 保存坐标系面积的列表
    axis_projection_list = [] # 保存坐标轴投影的列表
    axis_angle_list = []  # 保存坐标系夹角的列表
    vector_list = []  # 向量的新坐标的列表
    dict_obj["group_name"] = group["group_name"]
    ori_axis = np.array(group["ori_axis"])
    vector = group["vectors"]
    tasks = group["tasks"]

    for task in tasks:
        if task["type"] == "change_axis":

            obj_axis = np.array(task["obj_axis"])
            obj_list.append(obj_axis) # 保存目标坐标系

            for vec in vector:
                # 坐标系转移
                new_vector = cv.change_axis(vec, ori_axis, obj_axis)
                vector_list.append(new_vector)
                # 向量与坐标轴的夹角
                old_vector = np.array(vec)
                axis_angle_list.append(cv.axis_angle(old_vector, obj_axis))
                axis_projection_list.append(cv.axis_projection(new_vector, ori_axis))


            # 坐标系面积
            area = abs(np.linalg.det(obj_axis))
            area_list.append(area)

            # 保存目标坐标系
            dict_obj["obj_axis"] = obj_list
            # 保存目标坐标系的面积
            dict_obj["area"] = area_list
            # 保存坐标系转移后的新坐标
            dict_obj["new_vector"] = vector_list
            # 保存向量与目标坐标系坐标轴的角度
            dict_obj["axis_angle"] = axis_angle_list
            # 保存向量与目标坐标系坐标轴的投影
            dict_obj["axis_projection"] = axis_projection_list


    # 保存一个任务的字典
    obj_dict_list.append(dict_obj)
#print(obj_dict_list)

# ---------------------- 导出到json文件 ----------------------------

from typing import Any, List, Dict

# ---------------------- 核心：递归转换所有NumPy类型为Python原生类型 ----------------------
def convert_numpy(obj: Any) -> Any:
    """
    递归处理所有数据类型：
    - np.ndarray → 保留4位小数的列表
    - np.float64/np.int64 → Python浮点数/整数
    - 列表/元组/字典 → 递归遍历
    - 其他原生类型 → 直接返回
    """
    # 处理NumPy数组
    if isinstance(obj, np.ndarray):
        return obj.round(4).tolist()
    # 处理NumPy数值类型
    elif isinstance(obj, (np.float64, np.float32, np.float16)):
        return float(obj)
    elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    # 处理列表/元组（递归）
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy(item) for item in obj]
    # 处理字典（递归）
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    # 原生类型（str/bool/None等）直接返回
    else:
        return obj

# ---------------------- 加载数据（若数据在文件中，需先读取） ----------------------
def load_data_from_file(file_path: str = "data.txt") -> List[Dict]:
    """
    从txt文件加载原始数据（你的数据保存在data.txt中）
    若数据已在内存中，可跳过此步骤直接使用原始数据
    """
    with open(file_path, "r", encoding="utf-8") as f:
        # 读取文件内容并执行（注意：仅信任本地合法数据）
        raw_content = f.read()
        # 替换数据中的np.xxx为实际可执行的numpy调用
        raw_content = raw_content.replace("np.float64", "np.float64").replace("array", "np.array")
        local_vars = {"np": np}
        exec(f"data = {raw_content}", globals(), local_vars)
        return local_vars["data"]

# ---------------------- 导出为JSON文件 ----------------------
def export_to_json(data: Any, save_path: str = "processed_all_tasks.json", indent: int = 4):
    """
    导出处理后的数据到JSON文件
    :param data: 原始数据（列表/字典，含NumPy类型）
    :param save_path: 保存路径
    :param indent: 格式化缩进，增强可读性
    """
    # 第一步：递归转换所有NumPy类型
    clean_data = convert_numpy(data)
    # 第二步：写入JSON文件
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(clean_data, f, ensure_ascii=False, indent=indent)
        print(f"✅ 数据成功导出到：{save_path}")
    except Exception as e:
        print(f"❌ 导出失败：{str(e)}")

export_to_json(obj_dict_list, "task_results.json")
