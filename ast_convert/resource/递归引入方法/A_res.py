import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp


@component(output_component_file='func_3_component.yaml', packages_to_install=['joblib'])
def func_3(func_3_output:Output[Dataset]):
    import joblib

    def func_2(a):

        def func_1(a, b):
            return (a + b)
        res = func_1(1, a)
        return res
    res = func_2(1)
    joblib.dump({'res': res}, func_3_output.path)
