# 脚本添加的导的kubeflow pipeline SDK需要导入的包
import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp

import requests
import numpy as np
import pandas as pd
# 生成的组件添加组件标识的装饰器，装饰器第一个参数是将此方法转换为组件yaml代码的文件名 第二个参数是当前组件需要用到的第三方包
@component(output_component_file='load_data_component.yaml', packages_to_install=['joblib', 'requests', 'numpy', 'pandas'])
# 组件方法定义   将原有方法的形参转换为输入元数据的形参并指定元数据类型为Input[Dataset]  并在形参上添加输出数据的元数据
def load_data(url_input:Input[Dataset], filename_input:Input[Dataset], url1_input:Input[Dataset], load_data_output:Output[Dataset]):
#     脚本扫描到当前组件所在源代码中引用的第三方包，然后将这些第三方包添加到组件方法内（因为组件方法外的包在组件打包的时候扫描不到）
    import requests
    import numpy as np
    import pandas as pd
    import joblib

    url = joblib.load(url_input.path)['url']
    filename = joblib.load(filename_input.path)['filename']
    url1 = joblib.load(url1_input.path)['url1']
    f = requests.get(url)
    with open(filename, 'wb') as code:
        code.write(f.content)
    a = pd.read_excel(filename)
    xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t', 'ck1', 'sk1', 'ck2', 'sk2']]
    ydata = np.log(a['Y'])
#     将组件的返回参数转化为字典的方式并落地到输出元数据指向的地方
    return joblib.dump({'xdata': xdata, ' ydata': ydata}, load_data_output.path)

@component(output_component_file='get_model1_component.yaml', packages_to_install=['joblib', 'requests', 'numpy', 'pandas'])
def get_model1(xdata_input:Input[Dataset], ydata_input:Input[Dataset], get_model1_output:Output[Dataset]):
    import requests
    import numpy as np
    import pandas as pd
    import joblib

    def load_data(url, filename: str, url1: int=10):
        f = requests.get(url)
        with open(filename, 'wb') as code:
            code.write(f.content)
        a = pd.read_excel(filename)
        xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t', 'ck1', 'sk1', 'ck2', 'sk2']]
        ydata = np.log(a['Y'])
        return (xdata, ydata)
    xdata = joblib.load(xdata_input.path)['xdata']
    ydata = joblib.load(ydata_input.path)['ydata']
    params = Parameters()
    params.add('beta0', value=1.0)
    params.add('beta1', value=1.0)
    params.add('beta6', value=1.0)
    params.add('ck1', value=1.0)
    params.add('sk1', value=1.0)
    params.add('ck2', value=1.0)
    params.add('sk2', value=1.0)
    load_data()
    model = minimize(load_data(), params, args=(xdata.values, ydata.values))
    return joblib.dump({'model': model}, get_model1_output.path)
