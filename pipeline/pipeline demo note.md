

kubeflow 官方文档 https://www.kubeflow.org/docs/

pipeline的API https://www.kubeflow.org/docs/components/pipelines/reference/api/kubeflow-pipeline-api-spec/

目前提交运行pipelines有2种方法，二者本质都是使用sdk编译pipelines组件。
(1)在notebook中使用sdk提交pipelines至服务中心，直接可以在UI中查看pipelines实验运行进度。
(2)将pipelines组件打成zip包通过ui上传至服务中心，同样可以在UI查看实验运行进度。



pipeline使用介绍。https://blog.csdn.net/qq_20466211/article/details/108609815



pipeline的单个组件可以进行打包，打包完成后是一个Yaml文件，我们可以将这些组件文件上传到一个github仓库或者是自建的组件仓库，当在构建pipeline过程中需要调用这些组件的时候直接从这些组件库总拉取相应的组件库就可以了。

也可以对单个组件单独的编写代码并单独打包成一个docker镜像，在需要调用的时候直接根据名字把他当成一个组件调用即可（在注解上注明他的镜像名字）



在创建pipeline的时候，使用SDK创建出来的Pipeline，编译之后的名字不能够是中文，不然会报错。

pipeline 一个pipeline文件中，可以同时实现几条pipeline线，他们可以互不相同



pipeline并不是单纯的DAG图，他还可以有环，根据环来循环直到达到跳出循环的条件



pipeline可以将一个功能组件打包成一个docker镜像，打包成镜像之后在创建pipeline的时候能够把他当成一个组件来调用，规定好输入输出即可。（那么在这个组件的内部就可以做一层缓存层，每次计算完成之后都将输入和输出存储到缓存，当输入匹配时可以直接调用已经计算过的结果）

通过PV操作来传输数据 https://blog.csdn.net/gzroy/article/details/115310991





我安装的kubeflow版本是1.4.0

kubeflow 官方文档https://v1-4-branch.kubeflow.org/。记得选1.4

kubeflow 文档https://www.bookstack.cn/read/kubeflow-1.3-en/55c08a37f631fc1c.md



如果需要jupyter直接操作pipeline需要在添加配置文件，并且在配置的时候选择上
