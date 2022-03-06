import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp
import  numpy as np
import pandas as pd
from lmfit import minimize, Parameters, Parameter, report_fit
from matplotlib.pylab import mpl
import matplotlib.pyplot as plt

@component(output_component_file='fun2min_component.yaml',packages_to_install=['lmfit','numpy','matplotlib','joblib','pandas',])
def fun2min(params1_path:Input[Dataset],x1_path:Input[Dataset],y1_path:Input[Dataset],fun2min_return: Output[Dataset]):
    import  numpy as np
    import pandas as pd
    from lmfit import minimize, Parameters, Parameter, report_fit
    from matplotlib.pylab import mpl
    import matplotlib.pyplot as plt
    import joblib
    params1=joblib.load(params1_path.path)["params1"]
    x1=joblib.load(x1_path.path)["x1"]
    y1=joblib.load(y1_path.path)["y1"]
    beta0 = params['beta0'].value
    beta1 = params['beta1'].value
    beta6 = params['beta6'].value
    ck1 = params['ck1'].value
    sk1 = params['sk1'].value
    ck2 = params['ck2'].value
    sk2 = params['sk2'].value
    model = beta0 + beta1 * x[:, 0] + beta6 * x[:, 5] + ck1 * x[:, 6] + sk1 * x[:, 7] + ck2 * x[:, 8] + sk2 * x[:, 9]
    joblib.dump({"model - y":model - y,},fun1min_return.path)


@component(output_component_file='fun1min_component.yaml',packages_to_install=['lmfit','numpy','matplotlib','joblib','pandas',])
def fun1min(params_path:Input[Dataset],x_path:Input[Dataset],y_path:Input[Dataset],fun1min_return: Output[Dataset]):
    import  numpy as np
    import pandas as pd
    from lmfit import minimize, Parameters, Parameter, report_fit
    from matplotlib.pylab import mpl
    import matplotlib.pyplot as plt
    import joblib
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
    params=joblib.load(params_path.path)["params"]
    x=joblib.load(x_path.path)["x"]
    y=joblib.load(y_path.path)["y"]
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
    joblib.dump({"model - y":model - y,},fun2min_return.path)




