import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp


@component(output_component_file='func_1_component.yaml', packages_to_install=['joblib'])
def func_1(a_input:Input[Dataset], b_input:Input[Dataset], func_1_output:Output[Dataset]):
    import joblib
    a = joblib.load(a_input.path)['a']
    b = joblib.load(b_input.path)['b']
    joblib.dump({'a + b': (a + b)}, func_1_output.path)

@component(output_component_file='func_2_component.yaml', packages_to_install=['joblib'])
def func_2(a_input:Input[Dataset], func_2_output:Output[Dataset]):
    import joblib
    a = joblib.load(a_input.path)['a']

    def func_1(a, b):
        return (a + b)
    res = func_1(1, a)
    joblib.dump({'res': res}, func_2_output.path)
