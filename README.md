# Kubeflow pipeline auto Construction



## 当前任务

+ 在解析python方法并转换为component组件的同时能够解析当前方法使用了那些方法，并将这些方法的源码找到，贴到当前方法里面。
+ 找到python方法代码中存在以参数形式传方法的情况并将所传方法的代码引入到当前的方法里面来

