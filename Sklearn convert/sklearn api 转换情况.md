# Skearn Api转换情况

转换的是sklearn源代码

https://scikit-learn.org.cn/view/45.html 用例

| 调用的方法                                                   | 结果截图                                                     | 结果 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| digits = datasets.load_digits()                              | ![image-20220319205208820](sklearn api 转换情况.assets/image-20220319205208820-7694330.png) | ✅    |
| data = digits.images.reshape((n_samples, -1))                | 没找到digits.images.reshape                                  | ❌    |
| classifier = svm.SVC(gamma=0.001)                            | SVC被添加到了需要使用到SVC类的方法中。不支持将一个类转换为一个组件。组件转换的基本单元是方法 | ✅    |
| train_test_split                                             | ![image-20220319211756735](sklearn api 转换情况.assets/image-20220319211756735-7695877.png) | ✅    |
| disp = metrics.plot_confusion_matrix(classifier, X_test, y_test) | ![image-20220319213900765](sklearn api 转换情况.assets/image-20220319213900765-7697142.png) | ✅    |



python import的底层逻辑是什么？ 是切换出去了还是将调用的代码引入进来。  每次将import的代码放进来还是怎么搞的 是否是冗余

kubeflow 组件之间的调用是否能够有。组件内调用组件就出现耦合了



将sklearn的那个demo 把能替换的地方就替换掉https://scikit-learn.org.cn/view/45.html

将这个demo跑在pipeline里面

画图的代码应该进行图片落地



