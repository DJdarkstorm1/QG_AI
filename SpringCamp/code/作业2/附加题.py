"""
附加题
"""
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif

# 获取数据
train_df = pd.read_csv("./train.csv")
test_df = pd.read_csv("./test_features.csv")
# 数据处理
train_df['label'] = train_df['target'].map({-1: 0, 1: 1})# 加了1标签列

x = train_df.iloc[:, :-2]
y = train_df['label']
x_test_feature = test_df

# transfer = PCA(n_components=50)
# x_pca = transfer.fit_transform(x)
# x_test_feature_pca = transfer.transform(x_test_feature)

# 1. 先从 10000 维 选出 200 维
selector = SelectKBest(f_classif, k=50)
x_selected = selector.fit_transform(x, y)
x_test_feature_selected = selector.transform(x_test_feature)
# 2. 再 PCA 降到 50 维
pca = PCA(n_components=50)
x_pca = pca.fit_transform(x_selected)
x_test_feature_pca = pca.transform(x_test_feature_selected)
# 数据集划分
x_train, x_test, y_train, y_test = train_test_split(x_pca, y, test_size = 0.2, random_state = 0)

# 预估器
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=10,
    min_samples_split=2)
model.fit(x_train, y_train)

predictions = model.predict(x_test_feature_pca)

score = model.score(x_test, y_test)
print("score", score)

submission = pd.DataFrame({
    'id': np.arange(1, len(predictions)+1),
    'label': predictions
})

submission.to_csv('submission.csv', index=False)