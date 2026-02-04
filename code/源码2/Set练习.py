# 覆盖全集的最小子集合

U={1,2,3,4,5}
S=[{1,2,3},{2,4},{3,4},{4,5}]

for i in S:
    for j in S:
        if i|j==U:
            print(f"S=[{i},{j}]")

# 有一个组合生成器可以轻松解决
'''
from itertools import combinations

def find_min_set_cover(universe, subsets):
    """
    寻找覆盖全集的最小子集组合
    :param universe: 全集（集合类型，如 {1,2,3,4,5}）
    :param subsets: 待选子集列表（元素为集合类型，如 [{1,2,3}, {2,4}, ...]）
    :return: 最小子集组合（列表），若无法覆盖返回空列表
    """
    # 遍历子集数量：从1个开始，逐步增加（保证找到的是最小组合）
    for k in range(1, len(subsets) + 1):
        # 生成所有k个子集的组合
        for combo in combinations(subsets, k):
            # 计算当前组合的并集
            union_set = set().union(*combo)
            # 并集等于全集，说明找到最小覆盖
            if union_set == universe:
                return list(combo)
    # 所有组合都无法覆盖全集
    return []

# ------------------- 测试本题场景 -------------------
if __name__ == "__main__":
    U = {1, 2, 3, 4, 5}  # 全集
    S = [{1,2,3}, {2,4}, {3,4}, {4,5}]  # 待选子集（统一为集合，避免列表报错）
    
    min_cover = find_min_set_cover(U, S)
    if min_cover:
        print(f"找到覆盖全集的最小子集组合，共{len(min_cover)}个子集：")
        for idx, s in enumerate(min_cover, 1):
            print(f"第{idx}个子集：{s}")
    else:
        print("没有找到能覆盖全集的子集组合")
'''