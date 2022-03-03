import  numpy as np
import pandas as pd
from lmfit import minimize, Parameters, Parameter, report_fit
from matplotlib.pylab import mpl
import matplotlib.pyplot as plt

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

def fun1min(params, x, y):
    beta0 = params['beta0'].value
    beta1 = params['beta1'].value
    beta6 = params['beta6'].value
    ck1 = params['ck1'].value
    sk1 = params['sk1'].value
    ck2 = params['ck2'].value
    sk2 = params['sk2'].value
    model = beta0 + beta1 * x[:, 0] + beta6 * x[:, 5] + ck1 * x[:, 6] + sk1 * x[:, 7] + ck2 * x[:, 8] + sk2 * x[:, 9]
    fun2min(model - y)
    func1(func2())
    return model - y




