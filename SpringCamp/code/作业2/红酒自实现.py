"""
自实现线性\逻辑回归 + 红酒质量分析
"""
import numpy as np
import pandas as pd

class SelfLinearRegression:
    def __init__(self, add_bias=True):
        self.add_bias = add_bias
        self.weights = None
        self.bias = None

    def _add_bias(self, x):
        """
        偏置项
        :param x:
        :return:
        """
        if self.add_bias:
            return np.column_stack([np.ones(x.shape[0]), x])
        return x

    def fit1(self, x, y):
        """
        正规方程
        :param x:
        :param y:
        :return:
        """
        x_bias = self._add_bias(x)
        # 正规方程
        self.weights = np.linalg.pinv(x_bias) @ y

    def fit2(self, x_train, y_train, learning_rate=0.01, epochs=1000):
        """
        梯度下降
        :param x_train: 特征
        :param y_train: 标签
        :param learning_rate: 学习率
        :param epochs: 迭代次数
        :return:
        """
        x_train = np.asarray(x_train)
        y_train = np.asarray(y_train).flatten()  # 确保是一维

        if x_train.ndim == 1:
            x_train = x_train.reshape(-1, 1)

        n_samples, n_features = x_train.shape

        # 初始化权重（包含偏置）
        self.weights = np.zeros(n_features + 1)

        # 添加偏置列
        x_train_with_bias = self._add_bias(x_train)

        # 梯度下降迭代
        for i in range(epochs):
            # 前向传播：计算预测值
            y_pred = x_train_with_bias @ self.weights

            # 计算梯度
            dw = (2 / n_samples) * (x_train_with_bias.T @ (y_pred - y_train))

            # 更新参数
            self.weights -= learning_rate * dw

            # 可选：打印损失
            if (i + 1) % 1000 == 0:
                loss = np.mean((y_pred - y_train) ** 2)
                print(f"Epoch {i + 1}/{epochs}, Loss: {loss:.6f}")

    def predict(self, x):
        """
        预测函数
        :param x:
        :return: 一维数组
        """
        x = np.asarray(x)
        if x.ndim == 1:
            x = x.reshape(-1, 1)
        x_bias = self._add_bias(x)
        # 返回一维数组
        return (x_bias @ self.weights).flatten()

    def get_coef(self):
        """
        获取系数
        :return:
        """
        if self.add_bias:
            return self.weights[1:],self.weights[0]
        return self.weights,0

class SelfLogisticRegressor:
    def __init__(self, learnning_rate = 0.01, n_iteration = 10000, add_bias=True):
        self.learnning_rate = learnning_rate
        self.n_iteration = n_iteration
        self.add_bias = add_bias
        self.weights = None
        self.loss_history = []

    def _sigmoid(self, x):
        """
        激活函数sigmoid
        :param x:
        :return:
        """
        return 1 / (1 + np.exp(-x))

    def _add_bias(self, x):
        if self.add_bias:
            return np.column_stack([np.ones(x.shape[0]), x])
        return x

    def fit(self, x, y):
        """
        梯度下降
        :param x:
        :param y:
        :return:
        """
        x_bias = self._add_bias(x)
        n_samples, n_features = x_bias.shape

        self.weights = np.zeros(n_features)
        for i in range(self.n_iteration):
            linear_output = x_bias @ self.weights
            y_hat = self._sigmoid(linear_output)

            # 计算梯度
            gradient = ( 1/ n_samples) * x_bias.T @ (y_hat - y)

            # 更新参数
            self.weights -= self.learnning_rate * gradient

            # 计算损失
            loss = self._compute_loss(y, y_hat)
            self.loss_history.append(loss)

    def _compute_loss(self, y, y_hat):
        """
        损失函数
        :param y:
        :param y_hat:
        :return:
        """
        return -np.mean(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))

    def predict_probability(self, x):
        """
        计算概率
        :param x:
        :return:
        """
        x_bias = self._add_bias(x)
        linear_output = x_bias @ self.weights
        return self._sigmoid(linear_output)

    def predict(self, x, threshold = 0.5):
        """
        分类
        :param x:
        :param threshold:
        :return:
        """
        proba = self.predict_probability(x)
        return (proba >= threshold).astype(int)

    def get_coef(self):
        """
        获取参数
        :return:
        """
        if self.add_bias:
            return self.weights[1:],self.weights[0]
        return self.weights,0

# 标准化
def standardize(x):
    mean = np.mean(x,axis=0)
    std = np.std(x,axis=0)
    x_std = (x - mean) / std
    return x_std
# 数据集划分
def train_test_split(x, y, pec = 0.8, random_seed = 42):
    """
    划分数据集
    :param x: 特征集
    :param y: 标签集
    :param pec: 划分比例
    :param random_seed:随机种子
    :return: 训练集，测试集
    """
    np.random.seed(random_seed)
    n_data = len(x)
    idx = np.random.permutation(n_data)
    train_pec = pec
    train_idx = idx[:int(n_data*train_pec)]
    test_idx = idx[int(n_data*train_pec):]
    x_train = x.iloc[train_idx]
    y_train = y.iloc[train_idx]
    x_test = x.iloc[test_idx]
    y_test = y.iloc[test_idx]
    return x_train, y_train, x_test, y_test
# MSE参数
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
# R^2参数
def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot

# 逻辑回归评估指标
def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def precision(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    return tp / (tp + fp) if (tp + fp) > 0 else 0

def recall(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp / (tp + fn) if (tp + fn) > 0 else 0

def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * p * r / (p + r) if (p + r) > 0 else 0

if __name__ == '__main__':
    # 获取数据
    wine = pd.read_csv('winequality-red.csv', sep=';')

    # 数据处理
    x = wine.drop("quality", axis=1)
    y_ori = wine["quality"]
    wine['quality'] = (wine['quality'] > 6).astype(int)
    y = wine["quality"]
    # 标准化
    x_std = standardize(x)

    # 划分训练集
    x_train, y_train, x_test, y_test =train_test_split(x_std, y, pec = 0.8, random_seed = 0)

    # 预估器
    estimator = SelfLinearRegression()
    estimator.fit2(x_train, y_train)
    estimator2 = SelfLogisticRegressor()
    estimator2.fit(x_train, y_train)

    # 模型评估
    w, b = estimator.get_coef()
    print("线性回归系数：",w)
    print("偏置：",b)
    y_hat = estimator.predict(x_test)
    print("MSE:",mse(y_test, y_hat))
    print("R2:",r2_score(y_test, y_hat))

    print("逻辑回归",)
    w1, b1 = estimator2.get_coef()
    print("系数：",w1)
    print("偏置：",b1)
    y_hat2 = estimator2.predict(x_test)
    y_hat_train = estimator2.predict(x_train)
    print(f"  训练集 - 准确率: {accuracy(y_train, y_hat_train):.4f}")
    print(f"  测试集 - 准确率: {accuracy(y_test, y_hat2):.4f}")
    print(f"  测试集 - 精确率: {precision(y_test, y_hat2):.4f}")
    print(f"  测试集 - 召回率: {recall(y_test, y_hat2):.4f}")
    print(f"  测试集 - F1分数: {f1_score(y_test, y_hat2):.4f}")




