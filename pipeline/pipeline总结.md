# pipeline总结



## 代码结构

代码一共分为五部分/六部分

​	如果分为五部分的话就是用户提交脚本之后对脚本编译成Python代码，经过执行之后返回yaml文件，用户自行去执行界面提交和运行，这样的好处是执行是可控的，可归纳的。用户可以将一个pipeline提交到pipeline中，对pipeline进行统一管理，能够将pipeline归类到一个具体的experiment中运行。

​	如果是分为六部分的话就需要再加一个直接run的部分，这部分获取pipeline连接并直接run，这样提交大pipeline只会出现在run部分，不会出现在pipeline部分，不会属于一个既定的experiment。

​	 下面将统一列举代码的结构，所有部分的代码结构都是既定的，也就是结构化的代码。

+ 导包部分
	+ 因为pipeline使用到的包都是既定的，不需要进行修改，因此这部分的代码都是静态的。
+ 导入组件部分
	+ 每次不同的是组件的名字和加载组件的url，其他的都是相同的
+ 定义pipeline装饰器部分
	+ 这一部分只有一行代码，是写在pipeline方法定义上的装饰器，只要内容是定义pipeline的名字和description
+ 定义pipeline方法部分
	+ 这一部分变化的是方法名和参数，参数有不确定个，并且每个参数都应该设置默认值（可当作初始值）。
+ pipeline方法体部分
	+ 方法体部分，每一行都是对一个组件的调用，调用分为返回变量名，组件方法体，组件参数。
	+ 组件的参数分为两类：
		+ pipeline方法体参数
		+ 其他组件的返回值参数
+ 运行pipeline部分
	+ 代码只需要修改的只是pipeline的方法名，其他的都是静态代码





## 脚本程序的设计思路

首先从pipeline的顶层开始往下设计，需要一个pipeline对整个pipeline的基本结构进行描述。

因此在pipeline中整体结构如下所示：

```json
"pipeline":{
    "components": //描述的是当前pipeline所包含的组件信息，一个list，里面的对象一个是具体的调用组件
    [
      {
        "componentInputParams":  //组件的输入参数，里面的一个对象是组件调用方法的一个参数
          [
              {
                "name": "a",  //参数的输入名
                "pipelineParam": true, //参数是否为pipeline方法参数,为True表示是使用的pipeline的方法参数，false表示使用的是上一个组件的参数
                "pipelineParamName": "a" //输入的pipeline方法声明的参数名def funcName(a,b)
              },
              {
                "name": "b", 
                "pipelineParam": true,
                "pipelineParamName": "b"
              }
        ],
        "funcName": "add", //组件的方法名，一个组件有一个独一无二的方法名，相同组件的方法名一样
        "id": "1", //组件的ID 
        "name": "addparams", //组件名
        "url": "http://10.23.71.70/kubeflow/pipeline/addcomponent.yml" //加载组件的URL
      },
      {
        "componentInputParams": [
          {
            "name": "a",
            "pipelineParam": false,
            "originCompoId": "1" // 这个组件的当前输入参数是指定id组件的输出参数
          },
          {
            "name": "b",
            "pipelineParam": false,
            "originCompoId": "1"
          }
        ],
        "funcName": "add", 
        "id": "2",
        "name": "addparams",
        "url": "http://10.23.71.70/kubeflow/pipeline/addcomponent.yml"
      },
      {
        "componentInputParams": [
          {
            "name": "a",
            "pipelineParam": false,
            "originCompoId": "1"
          },
          {
            "name": "b",
            "pipelineParam": false,
            "originCompoId": "2"
          }
        ],
        "funcName": "add",
        "id": "3",
        "name": "addparams",
        "url": "http://10.23.71.70/kubeflow/pipeline/addcomponent.yml"
      },
      {
        "componentInputParams": [
          {
            "name": "a",
            "pipelineParam": false,
            "originCompoId": "2"
          },
          {
            "name": "b",
            "pipelineParam": false,
            "originCompoId": "1"
          }
        ],
        "funcName": "add",
        "id": "4",
        "name": "addparams",
        "url": "http://10.23.71.70/kubeflow/pipeline/addcomponent.yml"
      },
      {
        "componentInputParams": [
          {
            "name": "a",
            "pipelineParam": false,
            "originCompoId": "4"
          },
          {
            "name": "b",
            "pipelineParam": false,
            "originCompoId": "2"
          }
        ],
        "funcName": "sub",
        "id": "5",
        "name": "subparams",
        "url": "http://10.23.71.70/kubeflow/pipeline/subcomponent.yml"
      }
    ],
    "description": "it's my first test to build a pipeline",  //pipeline的形容信息
    "pipelineFuncName": "firstpipeline", //pipeline的方法名
    "pipelineName": "simplepipeline", //pipeline的名字
    "pipelineParams": [ //pipeline方法的参数信息
      {
        "defaultValue": "10", //默认值/初始值
        "name": "a", //参数名
        "type": "int" //参数类型
      },
      {
        "defaultValue": "10", 
        "name": "b",
        "type": "int"
      }
    ]
  }
```

