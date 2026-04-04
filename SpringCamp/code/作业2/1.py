import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.preprocessing import StandardScaler

# 加载数据
train_df = pd.read_csv("./train.csv")
test_df = pd.read_csv("./test_features.csv")

# 标签处理
train_df['label'] = train_df['target'].map({-1: 0, 1: 1})
x = train_df.iloc[:, :-2]
y = train_df['label']
x_test = test_df

# 标准化（PCA前必须做）
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
x_test_scaled = scaler.transform(x_test)

# 特征选择：保留1000个最佳特征
selector = SelectKBest(mutual_info_classif, k=500)
x_selected = selector.fit_transform(x_scaled, y)
x_test_selected = selector.transform(x_test_scaled)

# PCA：保留95%方差
pca = PCA(n_components=0.95)
x_pca = pca.fit_transform(x_selected)
x_test_pca = pca.transform(x_test_selected)

print(f"原始维度: {x.shape[1]}")
print(f"选择后维度: {x_selected.shape[1]}")
print(f"PCA后维度: {x_pca.shape[1]}")

# 划分训练集和验证集
x_train, x_val, y_train, y_val = train_test_split(
    x_pca, y, test_size=0.2, random_state=42, stratify=y  # 加上stratify保持类别比例
)

# 训练模型
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42,
)

model.fit(x_train, y_train)

# 验证分数
train_score = model.score(x_train, y_train)
val_score = model.score(x_val, y_val)
print(f"训练集准确率: {train_score:.4f}")
print(f"验证集准确率: {val_score:.4f}")

# 交叉验证
cv_scores = cross_val_score(model, x_pca, y, cv=8)
print(f"5折交叉验证: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")



# # 预测
# predictions = model.predict(x_test_pca)
#
# # 提交
# submission = pd.DataFrame({
#     'id': np.arange(1, len(predictions) + 1),
#     'label': predictions
# })
# submission.to_csv('submission.csv', index=False)