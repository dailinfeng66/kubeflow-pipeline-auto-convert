import requests
import numpy as np
import pandas as pd
def load_data(url,filename:str,url1:int = 10):
    f = requests.get(url)
    with open(filename, 'wb') as code:
        code.write(f.content)
    a = pd.read_excel(filename)
    xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t','ck1', 'sk1', 'ck2', 'sk2']]
    ydata = np.log(a["Y"])
    return xdata,ydata

def get_model1(xdata,ydata):
    params = Parameters()
    params.add('beta0', value= 1.)
    params.add('beta1', value= 1.)
    params.add('beta6', value= 1.)
    params.add('ck1', value= 1.)
    params.add('sk1', value= 1.)
    params.add('ck2', value= 1.)
    params.add('sk2', value= 1.)

    model = minimize(fun1min, params, args = (xdata.values, ydata.values))

    return model

def load_data(url,filename:str,url1:int = 10):
    f = requests.get(url)
    with open(filename, 'wb') as code:
        code.write(f.content)
    a = pd.read_excel(filename)
    xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t','ck1', 'sk1', 'ck2', 'sk2']]
    ydata = np.log(a["Y"])
    return xdata,ydata