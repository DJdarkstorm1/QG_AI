from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def knn_iris():
    """
    KNN分类
    :return:
    """
    # 获取数据
    iris = load_iris()
    # 划分数据集
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=10)
    # 标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train) # 训练集转换并生成模型
    x_test = transfer.transform(x_test) # 测试集仅转换 便于比较
    # 预估器
    estimator = KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train, y_train)
    # 模型评估
    # 1.直接比较
    y_predict = estimator.predict(x_test)
    print("y_predict:\n", y_predict)
    print("直接对比", y_test == y_predict)
    # 2.计算准确率
    score = estimator.score(x_test, y_test)
    print("score:", score)
    return None

def knn_iris_gscv():
    """
    KNN分类 + 交叉验证 + 网格搜索
    :return:
    """
    # 获取数据
    iris = load_iris()
    # 划分数据集
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=22)
    # 标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train) # 训练集转换并生成模型
    x_test = transfer.transform(x_test) # 测试集仅转换 便于比较
    # 预估器
    estimator = KNeighborsClassifier() # n_neighbors=3设置k值

    # 网格搜索与交叉验证
    param_dict = {'n_neighbors': range(1, 11, 2)}
    estimator = GridSearchCV(estimator, param_grid=param_dict,cv=10)

    estimator.fit(x_train, y_train)
    # 模型评估
    # 1.直接比较
    y_predict = estimator.predict(x_test)
    print("y_predict:\n", y_predict)
    print("直接对比", y_test == y_predict)
    # 2.计算准确率
    score = estimator.score(x_test, y_test)
    print("score:", score)

    print("最佳参数:", estimator.best_params_)
    print("最佳结果:", estimator.best_score_)
    print("最佳估计器：", estimator.best_estimator_)
    print("交叉验证结果：", estimator.cv_results_)

    return None

def k_means_demo():
    """
    K-Means对鸢尾花分类
    :return:
    """
    # 获取数据
    iris = load_iris()

    # 预估器流程
    estimator = KMeans(n_clusters=4)
    estimator.fit(iris.data)
    y_predict = estimator.predict(iris.data)
    print("y_predict:\n", y_predict)

    # 模型评估：轮廓系数
    score = silhouette_score(iris.data, y_predict)
    print("silhouette_score:", score)

if __name__ == '__main__':
    print(__name__)
    # knn_iris()
    # knn_iris_gscv()
    k_means_demo()