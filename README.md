# Kubeflow pipeline auto Construction



## 当前任务

+ 在解析python方法并转换为component组件的同时能够解析当前方法使用了那些方法，并将这些方法的源码找到，贴到当前方法里面。
+ 找到python方法代码中存在以参数形式传方法的情况并将所传方法的代码引入到当前的方法里面来



实现思路

我将会使用如下代码进行示例，

```python
def get_model1(xdata,ydata):
    params = Parameters()
    params.add('beta0', value= 1.)
    params.add('beta1', value= 1.)
    params.add('beta6', value= 1.)
    params.add('ck1', value= 1.)
    params.add('sk1', value= 1.)
    params.add('ck2', value= 1.)
    params.add('sk2', value= 1.)
    load_data()
    model = minimize(load_data(), params, args = (xdata.values, ydata.values))
    return model
```

上述代码在经过转换之后会如下所示：

```python
@component(output_component_file='get_model1_component.yaml',packages_to_install=['requests','numpy','joblib','pandas',])
def get_model1(xdata_path:Input[Dataset],ydata_path:Input[Dataset],get_model1_return: Output[Dataset]):
    import requests
    import numpy as np
    import pandas as pd
    import joblib
    def load_data(url,filename:str,url1:int = 10):
        f = requests.get(url)
        with open(filename, 'wb') as code:
            code.write(f.content)
        a = pd.read_excel(filename)
        xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t','ck1', 'sk1', 'ck2', 'sk2']]
        ydata = np.log(a["Y"])
        return xdata,ydata
    xdata=joblib.load(xdata_path.path)["xdata"]
    ydata=joblib.load(ydata_path.path)["ydata"]
    params = Parameters()
    params.add('beta0', value= 1.)
    params.add('beta1', value= 1.)
    params.add('beta6', value= 1.)
    params.add('ck1', value= 1.)
    params.add('sk1', value= 1.)
    params.add('ck2', value= 1.)
    params.add('sk2', value= 1.)
    load_data()
    model = minimize(load_data(), params, args = (xdata.values, ydata.values))
    joblib.dump({"model":model,},load_data_return.path)
```

  +  读取源代码，将源代码中的中文全部删除

  +  获取源代码文件中的导包语句 <code>import XXX</code> or <code>from xxx</code> ，并添加joblib包

	+ 获取导包语句目的：需要将用到的包添加到方法体里面去
	+ 添加joblib包的目的：在组件之间传递数据时将数据落地的方式

  +  扫描到方法的定义语句，修改方法定义语句中的参数。

	+  需要将参数转换为元数据读取的方式，因此每一个参数对应一个输入元数据，并且在方法的参数中添加一个输出元数据参数，用于将当前方法的返回值存到输出元数据指向的位置

	+  输入参数对应的元数据格式为：<code>param -> param_path:Input[Dataset]</code>

		输入出元数据对应的格式为：<code> funcName_return: Output[Dataset]</code>

		如

		```python
		def get_model1(xdata,ydata): 当前代码在经历这一步之后会转换为
		```

  +  在当前源代码的顶部添加编译当前代码为组件代码需要引入的包

  +  扫描到方法定义代码，在方法定义代码的上方添加组件定义的装饰器，并填写上相应的信息

	```python
	@component(output_component_file='get_model1_component.yaml',packages_to_install=['requests','numpy','joblib','pandas',])
	```

​			output_component_file为当前方法编译为组件时，组件yaml文件的名字，packages_to_install为当前组件需要用到的三方包，这些包不仅需要在方法内引入，还需要在组件定义的装饰器中声明，在装饰器中声明以后，当组件开始运行的时候组件内部才会使用install命令去安装这些包

+ 将原来方法代码的返回变量改为返回值落定并返回元数据的方式
	+ 扫描到返回值代码，考虑到返回值可能存在多个的情况，因此将返回值统一封装为字典形式，字典的key为返回值变量名，字典的value为返回值
	+ 使用joblib将字典存到指定的元数据存储位置（输入参数中的<code>funcName_return</code> ）

+ 还原组件参数变量：组件参数被修改为元数据之后参数名和参数的格式都发生了变化，因此代码能够运行还需要还原出原来的变量

	+ 原来的变量采用元数据的形式进行还原，使用joblib读取当前参数变量对应的元数据变量然后转换为当前的变量来实现变量还原

	+ 上一个组件的输出是使用joblib存储字典的方式，因此当前组件便是读取joblib并解析字典的方式还原出原来的变量

	+ 具体方式如下所示,原来是xdata,ydata是形参，现在由传入的元数据读取而来

	+ ```python
		xdata=joblib.load(xdata_path.path)["xdata"]
		ydata=joblib.load(ydata_path.path)["ydata"]
		```

+ 扫描当前文件的所有代码，获取到当前代码中调用了哪些当前代码中的方法，扫描到这些方法并将这些方法写到当前方法的导包代码之后，具体的操作结果如下所示

	```python
	def get_model1(xdata_path:Input[Dataset],ydata_path:Input[Dataset],get_model1_return: Output[Dataset]):
	    import requests
	    import numpy as np
	    import pandas as pd
	    import joblib
	    def load_data(url,filename:str,url1:int = 10):
	        f = requests.get(url)
	        with open(filename, 'wb') as code:
	            code.write(f.content)
	        a = pd.read_excel(filename)
	        xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t','ck1', 'sk1', 'ck2', 'sk2']]
	        ydata = np.log(a["Y"])
	        return xdata,ydata
	```

	

	  
