import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp
import requests
import numpy as np
import pandas as pd
@component(output_component_file='load_data_component.yaml',packages_to_install=['requests','numpy','joblib','pandas',])
def load_data(url_path:Input[Dataset],filename_path:Input[Dataset],url1_path:Input[Dataset],load_data_return: Output[Dataset]):
    import requests
    import numpy as np
    import pandas as pd
    import joblib
    url=joblib.load(url_path.path)["url"]
    filename=joblib.load(filename_path.path)["filename"]
    url1=joblib.load(url1_path.path)["url1"]
    f = requests.get(url)
    with open(filename, 'wb') as code:
        code.write(f.content)
    a = pd.read_excel(filename)
    xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t','ck1', 'sk1', 'ck2', 'sk2']]
    ydata = np.log(a["Y"])
    joblib.dump({"xdata":xdata,"ydata":ydata,},get_model1_return.path)

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

