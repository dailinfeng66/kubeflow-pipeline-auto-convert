import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.pylab import mpl



xdata = a[['t', 'X_t_1', 'X_t_2', 't_T_1_X_t_1', 't_T_2_X_t_2', 'H_t','ck1', 'sk1', 'ck2', 'sk2']]
x = xdata.values
ydata = np.log(a["Y"])
y = ydata.values

@component(output_component_file='fun1_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def fun1(x_path:Input[Dataset],b0_path:Input[Dataset],b1_path:Input[Dataset],b6_path:Input[Dataset],c1_path:Input[Dataset],s1_path:Input[Dataset],c2_path:Input[Dataset],s2_path:Input[Dataset],fun1_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    x=joblib.load(x_path.path)["x"]
    b0=joblib.load(b0_path.path)["b0"]
    b1=joblib.load(b1_path.path)["b1"]
    b6=joblib.load(b6_path.path)["b6"]
    c1=joblib.load(c1_path.path)["c1"]
    s1=joblib.load(s1_path.path)["s1"]
    c2=joblib.load(c2_path.path)["c2"]
    s2=joblib.load(s2_path.path)["s2"]
    joblib.dump({"b0 + b1 * x[0] + b6 * x[5] \":b0 + b1 * x[0] + b6 * x[5] \,},plt_final_results_return.path)
          + c1 * x[6] + s1 * x[7] + c2 * x[8] + s2 * x[9]

@component(output_component_file='fun2_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def fun2(x_path:Input[Dataset],b0_path:Input[Dataset],b1_path:Input[Dataset],b2_path:Input[Dataset],b4_path:Input[Dataset],b6_path:Input[Dataset],c1_path:Input[Dataset],s1_path:Input[Dataset],c2_path:Input[Dataset],s2_path:Input[Dataset],fun2_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    x=joblib.load(x_path.path)["x"]
    b0=joblib.load(b0_path.path)["b0"]
    b1=joblib.load(b1_path.path)["b1"]
    b2=joblib.load(b2_path.path)["b2"]
    b4=joblib.load(b4_path.path)["b4"]
    b6=joblib.load(b6_path.path)["b6"]
    c1=joblib.load(c1_path.path)["c1"]
    s1=joblib.load(s1_path.path)["s1"]
    c2=joblib.load(c2_path.path)["c2"]
    s2=joblib.load(s2_path.path)["s2"]
    joblib.dump({"b0 + b1 * x[0] + b2 * x[1] + b4 * x[3] + b6 * x[5] \":b0 + b1 * x[0] + b2 * x[1] + b4 * x[3] + b6 * x[5] \,},plt_results_return.path)
          + c1 * x[6] + s1 * x[7] + c2 * x[8] + s2 * x[9]

@component(output_component_file='fun3_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def fun3(x_path:Input[Dataset],b0_path:Input[Dataset],b1_path:Input[Dataset],b2_path:Input[Dataset],b3_path:Input[Dataset],b4_path:Input[Dataset],b5_path:Input[Dataset],b6_path:Input[Dataset],c1_path:Input[Dataset],s1_path:Input[Dataset],c2_path:Input[Dataset],s2_path:Input[Dataset],fun3_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    x=joblib.load(x_path.path)["x"]
    b0=joblib.load(b0_path.path)["b0"]
    b1=joblib.load(b1_path.path)["b1"]
    b2=joblib.load(b2_path.path)["b2"]
    b3=joblib.load(b3_path.path)["b3"]
    b4=joblib.load(b4_path.path)["b4"]
    b5=joblib.load(b5_path.path)["b5"]
    b6=joblib.load(b6_path.path)["b6"]
    c1=joblib.load(c1_path.path)["c1"]
    s1=joblib.load(s1_path.path)["s1"]
    c2=joblib.load(c2_path.path)["c2"]
    s2=joblib.load(s2_path.path)["s2"]
    joblib.dump({"b0 + b1 * x[0] + b2 * x[1] + b3 * x[2] + b4 * x[3] \":b0 + b1 * x[0] + b2 * x[1] + b3 * x[2] + b4 * x[3] \,},get_results_return.path)
         + b5 * x[4] + b6 * x[5] + c1 * x[6] + s1 * x[7] + c2 * x[8] + s2 * x[9]

@component(output_component_file='fun1_wrapper_for_odr_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def fun1_wrapper_for_odr(beta_path:Input[Dataset],x_path:Input[Dataset],fun1_wrapper_for_odr_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    def fun1(x, b0, b1, b6, c1, s1, c2, s2):
        return b0 + b1 * x[0] + b6 * x[5] \
              + c1 * x[6] + s1 * x[7] + c2 * x[8] + s2 * x[9]
    beta=joblib.load(beta_path.path)["beta"]
    x=joblib.load(x_path.path)["x"]
    joblib.dump({"fun1(x":fun1(x,"*beta)":*beta),},fun3_wrapper_for_odr_return.path)

@component(output_component_file='fun2_wrapper_for_odr_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def fun2_wrapper_for_odr(beta_path:Input[Dataset],x_path:Input[Dataset],fun2_wrapper_for_odr_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    def fun2(x, b0, b1, b2, b4, b6, c1, s1, c2, s2):
        return b0 + b1 * x[0] + b2 * x[1] + b4 * x[3] + b6 * x[5] \
              + c1 * x[6] + s1 * x[7] + c2 * x[8] + s2 * x[9]
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    beta=joblib.load(beta_path.path)["beta"]
    x=joblib.load(x_path.path)["x"]
    joblib.dump({"fun2(x":fun2(x,"*beta)":*beta),},fun2_wrapper_for_odr_return.path)

@component(output_component_file='fun3_wrapper_for_odr_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def fun3_wrapper_for_odr(beta_path:Input[Dataset],x_path:Input[Dataset],fun3_wrapper_for_odr_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    def fun3(x, b0, b1, b2, b3, b4, b5, b6, c1, s1, c2, s2): 
        return b0 + b1 * x[0] + b2 * x[1] + b3 * x[2] + b4 * x[3] \
             + b5 * x[4] + b6 * x[5] + c1 * x[6] + s1 * x[7] + c2 * x[8] + s2 * x[9]
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    beta=joblib.load(beta_path.path)["beta"]
    x=joblib.load(x_path.path)["x"]
    joblib.dump({"fun3(x":fun3(x,"*beta)":*beta),},fun1_wrapper_for_odr_return.path)

@component(output_component_file='get_results_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def get_results(fun_wrapper_for_odr_path:Input[Dataset],x_path:Input[Dataset],y_path:Input[Dataset],params_path:Input[Dataset],param_names_path:Input[Dataset],get_results_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    fun_wrapper_for_odr=joblib.load(fun_wrapper_for_odr_path.path)["fun_wrapper_for_odr"]
    x=joblib.load(x_path.path)["x"]
    y=joblib.load(y_path.path)["y"]
    params=joblib.load(params_path.path)["params"]
    param_names=joblib.load(param_names_path.path)["param_names"]
    model = scipy.odr.odrpack.Model(fun_wrapper_for_odr)
    data = scipy.odr.odrpack.Data(x.T, y)
    myodr = scipy.odr.odrpack.ODR(data, model, beta0 = params,  maxit = 0)
    
    myodr.set_job(fit_type=2)
    
    parameterStatistics = myodr.run()
    df_e = len(x) - len(parameters)
    cov_beta = parameterStatistics.cov_beta
    sd_beta = parameterStatistics.sd_beta * parameterStatistics.sd_beta
    ci = []
    t_df = scipy.stats.t.ppf(0.975, df_e)

    for i in range(len(params)):
        ci.append([params[i] - t_df * parameterStatistics.sd_beta[i], params[i] + t_df * parameterStatistics.sd_beta[i]])

    tstat_beta = params / parameterStatistics.sd_beta # coeff t-statistics
    pstat_beta = (1.0 - scipy.stats.t.cdf(np.abs(tstat_beta), df_e)) * 2.0
    
    print('\t\t{}\t\t{}\t\t{}\t\t{}'.format('Coef.', 'P', 'L 95%CI', 'U 95%CI'))
    
    for i in range(len(params)):
        print('{}\t\t{:.3f}\t\t{:.4f}\t\t{:.3f}\t\t{:.3f}'.format(param_names[i], params[i], pstat_beta[i], ci[i][0], ci[i][1]))

@component(output_component_file='plt_results_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def plt_results(x_path:Input[Dataset],y_path:Input[Dataset],fun_path:Input[Dataset],params_path:Input[Dataset],start_path:Input[Dataset],end_path:Input[Dataset],plt_results_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    x=joblib.load(x_path.path)["x"]
    y=joblib.load(y_path.path)["y"]
    fun=joblib.load(fun_path.path)["fun"]
    params=joblib.load(params_path.path)["params"]
    start=joblib.load(start_path.path)["start"]
    end=joblib.load(end_path.path)["end"]
    plt.figure(figsize = (10, 8), dpi = 100)
    plt.plot(x[:, 0], y, 'b*', label = 'data')
    plt.plot(x[start:end, 0], fun(x.T, *params)[start:end])
    plt.axvline(55, color = "red", ls = "--")
    plt.axvline(63, color = "green", ls = "--")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Model Fitting")
    plt.show()
    def plt_final_results(x, y, fun1, params1, fun2, params2, fun3, params3):
        plt.figure(figsize = (10, 8), dpi = 100)
        plt.plot(xdata.values[:, 0], ydata.values, 'b*', label='data')
        plt.axvline(55,color="red",ls="--")
        plt.axvline(63,color="green",ls="--")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("Model Fitting")
        plt.legend()
        plt.show()
    params1, cov1 = curve_fit(fun1, x.T, y)
    params2, cov2 = curve_fit(fun2, x.T, y)
    params3, cov3 = curve_fit(fun3, x.T, y)
    param_names1 = ["beta0", "beta1", "vbeta6", "ck1", "sk1", "ck2", "sk2"]
    get_results(fun1_wrapper_for_odr, x, y, params1, param_names1)
    plt_results(x, y, fun1, params1, 55, 144)
    param_names2 = ["beta0", "beta1", "beta2", "beta4", "vbeta6", "ck1", "sk1", "ck2", "sk2"]
    get_results(fun2_wrapper_for_odr, x, y, params2, param_names2)
    plt_results(x, y, fun2, params2, 63, 144)
    param_names3 = ["beta0", "beta1", "beta2", "beta3", "beta4", "beta5", "vbeta6", "ck1", "sk1", "ck2", "sk2"]
    get_results(fun3_wrapper_for_odr, x, y, params3, param_names3)
    plt_results(x, y, fun3, params3, 0, 144)
    plt_final_results(x, y, fun1, params1, fun2, params2, fun3, params3)
    def plt_results(x, y, fun, params, start, end):
        plt.figure(figsize = (10, 8), dpi = 100)
        plt.plot(x[:, 0], y, 'b*', label = 'data')
        plt.plot(x[start:end, 0], fun(x.T, *params)[start:end])
        plt.axvline(55, color = "red", ls = "--")
        plt.axvline(63, color = "green", ls = "--")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("Model Fitting")
        plt.show()
    def get_results(fun_wrapper_for_odr, x, y, params, param_names):
        model = scipy.odr.odrpack.Model(fun_wrapper_for_odr)
        data = scipy.odr.odrpack.Data(x.T, y)
        myodr = scipy.odr.odrpack.ODR(data, model, beta0 = params,  maxit = 0)
        myodr.set_job(fit_type=2)
        parameterStatistics = myodr.run()
        df_e = len(x) - len(parameters)
        cov_beta = parameterStatistics.cov_beta
        sd_beta = parameterStatistics.sd_beta * parameterStatistics.sd_beta
        ci = []
        t_df = scipy.stats.t.ppf(0.975, df_e)
        for i in range(len(params)):
            ci.append([params[i] - t_df * parameterStatistics.sd_beta[i], params[i] + t_df * parameterStatistics.sd_beta[i]])
        tstat_beta = params / parameterStatistics.sd_beta # coeff t-statistics
        pstat_beta = (1.0 - scipy.stats.t.cdf(np.abs(tstat_beta), df_e)) * 2.0
        print('\t\t{}\t\t{}\t\t{}\t\t{}'.format('Coef.', 'P', 'L 95%CI', 'U 95%CI'))
        for i in range(len(params)):
            print('{}\t\t{:.3f}\t\t{:.4f}\t\t{:.3f}\t\t{:.3f}'.format(param_names[i], params[i], pstat_beta[i], ci[i][0], ci[i][1]))
    
@component(output_component_file='plt_final_results_component.yaml',packages_to_install=['numpy','matplotlib','scipy','joblib','pandas',])
def plt_final_results(x_path:Input[Dataset],y_path:Input[Dataset],fun1_path:Input[Dataset],params1_path:Input[Dataset],fun2_path:Input[Dataset],params2_path:Input[Dataset],fun3_path:Input[Dataset],params3_path:Input[Dataset],plt_final_results_return: Output[Dataset]):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from matplotlib.pylab import mpl
    import joblib
    x=joblib.load(x_path.path)["x"]
    y=joblib.load(y_path.path)["y"]
    fun1=joblib.load(fun1_path.path)["fun1"]
    params1=joblib.load(params1_path.path)["params1"]
    fun2=joblib.load(fun2_path.path)["fun2"]
    params2=joblib.load(params2_path.path)["params2"]
    fun3=joblib.load(fun3_path.path)["fun3"]
    params3=joblib.load(params3_path.path)["params3"]
    plt.figure(figsize = (10, 8), dpi = 100)
    plt.plot(xdata.values[:, 0], ydata.values, 'b*', label='data')
    plt.axvline(55,color="red",ls="--")
    plt.axvline(63,color="green",ls="--")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Model Fitting")
    plt.legend()
    plt.show()
    
params1, cov1 = curve_fit(fun1, x.T, y)
params2, cov2 = curve_fit(fun2, x.T, y)
params3, cov3 = curve_fit(fun3, x.T, y)

param_names1 = ["beta0", "beta1", "vbeta6", "ck1", "sk1", "ck2", "sk2"]

get_results(fun1_wrapper_for_odr, x, y, params1, param_names1)
plt_results(x, y, fun1, params1, 55, 144)

param_names2 = ["beta0", "beta1", "beta2", "beta4", "vbeta6", "ck1", "sk1", "ck2", "sk2"]

get_results(fun2_wrapper_for_odr, x, y, params2, param_names2)
plt_results(x, y, fun2, params2, 63, 144)

param_names3 = ["beta0", "beta1", "beta2", "beta3", "beta4", "beta5", "vbeta6", "ck1", "sk1", "ck2", "sk2"]

get_results(fun3_wrapper_for_odr, x, y, params3, param_names3)
plt_results(x, y, fun3, params3, 0, 144)

plt_final_results(x, y, fun1, params1, fun2, params2, fun3, params3)
