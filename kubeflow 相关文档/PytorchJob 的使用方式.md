# PythonchJob的使用方式

 [介绍和使用方式](https://www.kubeflow.org/docs/components/training/pytorch/)

[PytorchJob demo](https://github.com/kubeflow/training-operator/blob/master/examples/pytorch/simple.yaml)

[Kubeflow Training Operator](https://github.com/kubeflow/training-operator)

Kubeflow Training Operator 可以在K8s上运行分布式或者非分布式的Pytorch任务

[Kubeflow Training SDK](https://github.com/kubeflow/training-operator/tree/master/sdk/python)



# 分布式机器学习

简而言之，分布式机器学习主要是有两种，第一种是数据并行，第二种是模型并行。

**数据并行** 

将大规模的数据划分到不同的节点上进行并行训练。目前Pytorch已经有现成的数据并行的API。

Pytorch数据并行有DataParallel和DistributedDataParallel两种。DataParallel是在同一个机器上安装多张显卡，将数据分配到不同的显卡上进行计算。DistributedDataParallel是使用MPI实现CPU通信，通过NCCL实现GPU通信。可以用于单机多卡和多机多卡的情况。

> NCCL(Nvidia Collective multi-GPU Communication Library)
>
> 它是一个实现多GPU的collective communication通信（all-gather, reduce, broadcast）库.

**模型并行**

将大规模切分成若干子模型（包含一部分模型参数），将每个子模型放在一个工作节点上的方法。

