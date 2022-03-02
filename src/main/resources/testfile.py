import  numpy as np
import pandas as pd
from lmfit import minimize, Parameters, Parameter, report_fit
from matplotlib.pylab import mpl
import matplotlib.pyplot as plt




def fun1min(params, x, y):
    beta0 = params['beta0'].value
    beta1 = params['beta1'].value
    beta6 = params['beta6'].value
    ck1 = params['ck1'].value
    sk1 = params['sk1'].value
    ck2 = params['ck2'].value
    sk2 = params['sk2'].value
    model = beta0 + beta1 * x[:, 0] + beta6 * x[:, 5] + ck1 * x[:, 6] + sk1 * x[:, 7] + ck2 * x[:, 8] + sk2 * x[:, 9]
    return model - y,fun2min


def fun2min(params1, x1, y1):
    beta0 = params['beta0'].value
    beta1 = params['beta1'].value
    beta6 = params['beta6'].value
    ck1 = params['ck1'].value
    sk1 = params['sk1'].value
    ck2 = params['ck2'].value
    sk2 = params['sk2'].value
    model = beta0 + beta1 * x[:, 0] + beta6 * x[:, 5] + ck1 * x[:, 6] + sk1 * x[:, 7] + ck2 * x[:, 8] + sk2 * x[:, 9]
    return model - y


def load_data(url,filename:str,url1:int = 10):
    f = requests.get(url)
    with open(filename, 'wb') as code:
        code.write(f.content)
    a = pd.read_excel(filename)
    xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t','ck1', 'sk1', 'ck2', 'sk2']]
    ydata = np.log(a["Y"])
    return xdata,ydata