import  numpy as np
import pandas as pd
from lmfit import minimize, Parameters, Parameter, report_fit
from matplotlib.pylab import mpl
import matplotlib.pyplot as plt


def get_model3(xdata, ydata):

    # 参数定义及初始化
    params = Parameters()
    params.add('beta0', value= 1.)
    params.add('beta1', value= 1.)
    params.add('beta2', value= 1.)
    params.add('beta3', value= 1.)
    params.add('beta4', value= 1.)
    params.add('beta5', value= 1.)
    params.add('beta6', value= 1.)
    params.add('ck1', value= 1.)
    params.add('sk1', value= 1.)
    params.add('ck2', value= 1.)
    params.add('sk2', value= 1.)
    # 拟合优化函数
    model = minimize(fun3min, params, args = (xdata.values, ydata.values))
    return model1 , model2


def get_model1(data):
    xdata, ydata = data['xdata'],data['ydata']

    # 参数定义及初始化
    params = Parameters()
    params.add('beta0', value= 1.)
    params.add('beta1', value= 1.)
    params.add('beta6', value= 1.)
    params.add('ck1', value= 1.)
    params.add('sk1', value= 1.)
    params.add('ck2', value= 1.)
    params.add('sk2', value= 1.)

    # 拟合优化函数
    model = minimize(fun1min, params, args = (xdata.values, ydata.values))

    return model


def fun1min(params, x, y):
    beta0 = params['beta0'].value
    beta1 = params['beta1'].value
    beta6 = params['beta6'].value
    ck1 = params['ck1'].value
    sk1 = params['sk1'].value
    ck2 = params['ck2'].value
    sk2 = params['sk2'].value

    model = beta0 + beta1 * x[:, 0] + beta6 * x[:, 5] + ck1 * x[:, 6] + sk1 * x[:, 7] + ck2 * x[:, 8] + sk2 * x[:, 9]

    return model - y