"""
红酒品质线性回归
调参：学习率可以调
"""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pandas as pd

def linear_regression_demo():
    """
    波士顿房价线性回归+正规方程
    :return:
    """
    # 1.获取数据
    wine = pd.read_csv('./winequality-red.csv')

    # 2.数据处理
    x = wine[["volatile acidity","residual sugar", "pH", "alcohol"]]
    y = wine[["quality"]]
    x = x.to_dict(orient="records")
    # 3.数据集划分
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state =22)

    # 4.特征工程：标准化
    # 实例化
    transfer = StandardScaler()
    # 调用
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 5.预估器
    estimator = LinearRegression()
    estimator.fit(x_train, y_train)

    # 6.模型评估
    # 直接对比
    y_predict = estimator.predict(x_test)
    print("y_predict:", y_predict)
    print("直接对比:", y_test == y_predict )

    # 计算准确率
    score = estimator.score(x_test, y_test)
    print("score:", score)

    return None

if __name__ == '__main__':
    print()
    linear_regression_demo()
