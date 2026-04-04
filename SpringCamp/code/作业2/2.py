import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
from sklearn.model_selection import GridSearchCV
import warnings

warnings.filterwarnings('ignore')

# 读取数据
print("读取数据...")
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test_features.csv')

X_train = train_df.drop('target', axis=1)
y_train = train_df['target']
X_test = test_df.copy()
test_ids = np.arange(1, len(test_df) + 1)

print(f"训练集: {X_train.shape}, 测试集: {X_test.shape}")
print(f"标签类别: {y_train.unique()}")

# ============ 特征工程 ============
print("\n特征工程...")


def add_features(df):
    df = df.copy()
    # 基础统计
    df['row_sum'] = df.sum(axis=1)
    df['row_mean'] = df.mean(axis=1)
    df['row_std'] = df.std(axis=1)
    df['row_max'] = df.max(axis=1)
    df['row_min'] = df.min(axis=1)
    df['row_median'] = df.median(axis=1)
    # 非零统计
    df['nonzero_count'] = (df > 0).sum(axis=1)
    df['nonzero_ratio'] = df['nonzero_count'] / df.shape[1]
    df['zero_count'] = (df == 0).sum(axis=1)
    # 分位数
    df['q25'] = df.quantile(0.25, axis=1)
    df['q75'] = df.quantile(0.75, axis=1)
    df['iqr'] = df['q75'] - df['q25']
    # 极值特征
    df['max_min_ratio'] = df['row_max'] / (df['row_min'] + 1e-6)
    return df


X_train = add_features(X_train)
X_test = add_features(X_test)

print(f"特征数: {X_train.shape[1]}")

# ============ 特征选择 ============
print("\n特征选择...")

# 移除低方差特征
selector = VarianceThreshold(threshold=0.01)
X_train_var = selector.fit_transform(X_train)
X_test_var = selector.transform(X_test)
print(f"方差过滤后: {X_train_var.shape[1]}")

# 选择最重要的特征
k = min(50, X_train_var.shape[1])
selector_k = SelectKBest(f_classif, k=k)
X_train_sel = selector_k.fit_transform(X_train_var, y_train)
X_test_sel = selector_k.transform(X_test_var)
print(f"最终特征数: {X_train_sel.shape[1]}")

# ============ 标准化（SVM必须） ============
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_sel)
X_test_scaled = scaler.transform(X_test_sel)

# ============ SVM训练 ============
print("\n训练SVM...")

# 尝试不同的核函数
kernels = ['linear', 'rbf', 'poly']
best_score = 0
best_model = None
best_kernel = None

from sklearn.model_selection import cross_val_score

for kernel in kernels:
    print(f"\n尝试 {kernel} 核...")
    svm = SVC(kernel=kernel, random_state=42, max_iter=1000)
    scores = cross_val_score(svm, X_train_scaled, y_train, cv=5, scoring='accuracy')
    print(f"  {kernel}核: {scores.mean():.4f} (+/- {scores.std():.4f})")

    if scores.mean() > best_score:
        best_score = scores.mean()
        best_model = svm
        best_kernel = kernel

print(f"\n最佳核函数: {best_kernel}, 准确率: {best_score:.4f}")

# 用最佳参数训练
best_model.fit(X_train_scaled, y_train)

# ============ 预测 ============
y_pred = best_model.predict(X_test_scaled)

# 保存结果
submission = pd.DataFrame({'id': test_ids, 'label': (y_pred==1).astype(int)})
submission.to_csv('submission.csv', index=False)

print("\n完成！")
print(f"预测分布:\n{submission['label'].value_counts().sort_index()}")
print(f"\n提交文件前10行:\n{submission.head()}")