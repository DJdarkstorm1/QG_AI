"""
一个自己实现的坐标转换类
"""
import numpy as np
from typing import Union


class CoordinateConvert:

    def __init__(self):
        self._last_transform_matrix = None

    @staticmethod
    def _is_valid_coordinate(axis: np.ndarray) -> bool:
        """
        私有方法：校验坐标系是否有效（核心条件）
        1. 是方阵（dim×dim）
        2. 基向量线性无关（行列式≠0）
        3. 无零向量基向量
        """
        try:
            # 校验是否为方阵
            if axis.ndim != 2 or axis.shape[0] != axis.shape[1]:
                return False
            dim = axis.shape[0]
            # 校验无零向量
            norms = np.linalg.norm(axis, axis=1)
            if np.any(norms < 1e-9):
                return False
            # 校验线性无关（行列式≠0）
            det = np.linalg.det(axis)
            return abs(det) > 1e-9
        except Exception:
            return False

    @staticmethod
    def normalize_axis(axis: np.ndarray) -> np.ndarray:
        """归一化坐标系的基向量（行=基向量）"""
        # 先转为np数组（兼容列表输入）
        axis = np.asarray(axis, dtype=np.float64)
        # 校验是否为有效坐标系（先校验，再归一化）
        if not CoordinateConvert._is_valid_coordinate(axis):
            raise ValueError("输入的坐标系无效（非方阵/线性相关/含零向量）")
        # 计算每个基向量的模长
        norms = np.linalg.norm(axis, axis=1)
        # 归一化：每个基向量 / 自身模长
        return axis / norms[:, np.newaxis]

    def change_axis(self,
                    vector: Union[list, np.ndarray],
                    src_axis: Union[list, np.ndarray],
                    dst_axis: Union[list, np.ndarray]) -> np.ndarray:
        """
        坐标系转移：将向量从源坐标系转换到目标坐标系
        :param vector: 源坐标系下的向量（支持一维/二维，行向量）
        :param src_axis: 源坐标系矩阵（dim×dim，行=基向量）
        :param dst_axis: 目标坐标系矩阵（dim×dim，行=基向量）
        :return: 目标坐标系下的向量（与输入vector维度一致）
        """
        # 1. 类型转换+维度统一
        vector = np.asarray(vector, dtype=np.float64)
        src_axis = np.asarray(src_axis, dtype=np.float64)
        dst_axis = np.asarray(dst_axis, dtype=np.float64)

        # 2. 维度校验
        dim = src_axis.shape[0]
        if dst_axis.shape[0] != dim:
            raise ValueError(f"源坐标系维度({dim})与目标坐标系维度({dst_axis.shape[0]})不匹配")
        # 处理向量维度
        is_1d = vector.ndim == 1
        if is_1d:
            if len(vector) != dim:
                raise ValueError(f"向量维度({len(vector)})与坐标系维度({dim})不匹配")
            vector = vector.reshape(1, -1)  # 转为二维行向量
        else:
            if vector.shape[1] != dim:
                raise ValueError(f"向量维度({vector.shape[1]})与坐标系维度({dim})不匹配")

        # 3. 归一化坐标系
        src_axis_norm = self.normalize_axis(src_axis)
        dst_axis_norm = self.normalize_axis(dst_axis)

        # 4. 计算转换矩阵
        try:
            src_axis_inv = np.linalg.inv(src_axis_norm.T)
        except np.linalg.LinAlgError:
            raise ValueError("源坐标系矩阵不可逆，基向量线性相关")
        transform_mat = src_axis_inv @ dst_axis_norm.T
        self._last_transform_matrix = transform_mat

        # 5. 转换向量并还原维度
        new_vector = vector @ transform_mat
        return new_vector.flatten() if is_1d else new_vector

    @staticmethod
    def axis_angle(vectors: Union[list, np.ndarray],
                   axis: Union[list, np.ndarray]) -> np.ndarray:
        """
        计算向量与坐标系各轴的夹角（返回角度，保留2位小数）
        :param vectors: 待计算向量（一维：(dim,) 或二维：(n, dim)）
        :param axis: 坐标系矩阵（dim×dim，行=基向量）
        :return: 夹角值（与输入维度一致）
        """
        # 类型转换+校验
        vectors = np.asarray(vectors, dtype=np.float64)
        axis = np.asarray(axis, dtype=np.float64)
        dim = axis.shape[0]
        if not CoordinateConvert._is_valid_coordinate(axis):
            raise ValueError("输入的坐标系无效")

        # 维度统一
        is_1d = vectors.ndim == 1
        if is_1d:
            if len(vectors) != dim:
                raise ValueError(f"向量维度({len(vectors)})与坐标系维度({dim})不匹配")
            vectors = vectors.reshape(1, -1)

        # 计算夹角
        angles = np.zeros_like(vectors, dtype=np.float64)
        vec_norms = np.linalg.norm(vectors, axis=1)
        axis_norms = np.linalg.norm(axis, axis=1)  # 行=基向量，所以axis=1

        for i in range(vectors.shape[0]):
            if vec_norms[i] < 1e-9:
                continue
            # 向量与每个行向量的点积
            dot_vals = np.dot(vectors[i], axis)
            cos_theta = dot_vals / (vec_norms[i] * axis_norms)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)
            angles[i] = np.arccos(cos_theta)

        # 转换为角度并还原维度
        angles = np.degrees(angles).round(2)
        return angles.flatten() if is_1d else angles

    @staticmethod
    def axis_projection(vectors: Union[list, np.ndarray],
                        axis: Union[list, np.ndarray]) -> np.ndarray:
        """
        计算向量在坐标系各轴的投影长度
        :param vectors: 待投影向量（一维：(dim,) 或二维：(n, dim)）
        :param axis: 坐标系矩阵（dim×dim，行=基向量）
        :return: 投影值
        """
        # 类型转换+校验
        vectors = np.asarray(vectors, dtype=np.float64)
        axis = np.asarray(axis, dtype=np.float64)
        dim = axis.shape[0]
        if not CoordinateConvert._is_valid_coordinate(axis):
            raise ValueError("输入的坐标系无效")

        # 维度统一
        is_1d = vectors.ndim == 1
        if is_1d:
            if len(vectors) != dim:
                raise ValueError(f"向量维度({len(vectors)})与坐标系维度({dim})不匹配")
            vectors = vectors.reshape(1, -1)

        # 计算投影
        n_vectors = vectors.shape[0]
        prj = np.zeros((n_vectors, dim), dtype=np.float64)
        axis_norms = np.linalg.norm(axis, axis=1)

        for i in range(n_vectors):
            dot_vals = np.dot(vectors[i], axis)
            prj_vals = np.where(axis_norms > 1e-9, dot_vals / axis_norms, 0.0)
            prj[i] = prj_vals

        return prj.flatten() if is_1d else prj
