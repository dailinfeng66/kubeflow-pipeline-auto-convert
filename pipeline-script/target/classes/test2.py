
import numpy as np
import pandas as pd
from lmfit import minimize, Parameters, Parameter, report_fit

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