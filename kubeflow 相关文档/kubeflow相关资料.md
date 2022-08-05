# kubeflow 相关资料

[云原生机器学习平台技术综述（编排调度篇）](https://zhuanlan.zhihu.com/p/544877743)

[**Common Problems with Creating Machine Learning Pipelines from Existing Code**](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/b50bc83882bbd29c50250d1e59fbc3afda3fb5e5.pdf)

ML编排系统的一个主要价值主张是提供一个框架，将各个工作流步骤定义为一个组件，以便每个步骤产生的数据可以被形式化，并且步骤可以跨不同的管道重用以提高效率。

将代码分解为逻辑工作流步骤，即组件。

ML模型的原型环境应该被设计成避免为了生产而从头重新实现的需要，2)ML管道应该提供一个预定义的规范操作单元的框架，作为组件，这样ML代码可以遵循ML工程的最佳实践，而不是自由形式的灵活性，3)组件之间的接口-代码和数据-应该足够明确和简单，以便实现这样的接口易于ML代码作者使用。

**End-to-end Machine Learning using Kubeflow**

这是一个kubeflow的教程



**Kubeflow for Machine Learning**

Kubeflow Pipeline 可以协调机器学习应用程序的执行。这个实现是基于Argo工作流的。Argo工作流是K8s的开源、容器原生工作流引擎。kubeflow安装了所有的Argo组件。

Kubeflow pipeline包含以下组件

+ Python SDK

	+ 使用Python代码创建Pipeline

+ DSL compiler

	+ 将Python编写的Pipeline代码转换为YAML描述文件

+ Pipeline Service

	+ 读取YAML配置文件创建Pipeline运行

+ Kubernetes resources

	+ Pipeline Service调用K8s的API来创建运行Pipeline所需的K8s自定义资源

+ *Orchestration controllers*

	+ 一组Orchestration controller执行完成K8s资源指定流水线执行所需的容器。这些容器在k8s的pod中执行。

+ *Artifact storage*

	k8s存储两种数据

	+ *Metadata*
		+ 实验、作业、运行等。Kubeflow Pipeline将原数据存储在mysql数据库中
	+ Artifacts
		+ 管道包、视图等。Kube-Flow管道将构件存储在诸如Minio服务器



## Pipelines





