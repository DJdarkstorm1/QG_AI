import numpy as np
arr = np.arange(12).reshape(3, 4)
print(arr)

print("shape:", arr.shape)
print("dtype:", arr.dtype)
print("ndim:", arr.ndim)

# 转置，变形为 (4,3)
arr_reshaped = arr.reshape(4, 3)
print("变形后：\n", arr_reshaped)

# 展平为一维数组
arr_flattened = arr_reshaped.flatten()
print("展平后：\n", arr_flattened)

# 转置，等价于 reshape(4, 3)
arr_reshape_neg = arr.reshape(4, -1)
print("使用 -1 变形后形状：", arr_reshape_neg.shape)