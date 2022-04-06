# 分类器的比较demo集成

<a href="https://scikit-learn.org.cn/view/47.html">demo链接</a>

在代码修改过程中遇到的问题：

| 问题                    | 解决办法                                                     |
| ----------------------- | ------------------------------------------------------------ |
| for循环应该怎么转换     | 在查阅kfp SDK源码的时候发现<br /><code>from kfp.dsl import (     graph_component,     pipeline,     Condition,     ContainerOp,     ExitHandler,     ParallelFor, )</code><br />表示kfp在定义组件的时候有这几种类型，ParallelFor在官方示例中没出现，在stackoverflow中找到示例发现是列表for循环的一种解决方式，顾名思义应该是并行for，那么只要不出现竞态条件就可以使用这个组件并行执行。<br /><a href="https://developer.ibm.com/blogs/kubeflow-pipelines-and-tekton-advances-data-workloads/#:~:text=The%20ParallelFor%20loop%20in%20Kubeflow%20Pipeline%20is%20a,tasks%20on%20a%20set%20of%20parameters%20in%20parallel.">一篇介绍文档</a> |
| 使用组件ParallelFor出错 | 使用ParallelFor的时候出错，无法run。暂时还没有找到解决办法   |
| if判断                  | dsl.Condition 官方有专门的if判断的方式，可以根据组件的返回值判断是否应该进入下面的组件运行 |



在代码转换中修改掉的地方

| 修改的地方               | 修改原因         |
| ------------------------ | ---------------- |
| 删掉了所有关于画图的代码 | 组件无法展示画图 |



方法转组件脚本修改：

| 修改的地方                                      | 改进                                                         |
| ----------------------------------------------- | ------------------------------------------------------------ |
| 每个方法component装饰器上需要的第三方包逻辑修改 | 之前版本会使得from x x x.xxx import xx识别第三方包为 x x x.xxx，现在改为正常识别 |

