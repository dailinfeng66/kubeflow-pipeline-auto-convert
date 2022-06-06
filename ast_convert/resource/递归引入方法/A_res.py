import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp

from resource.递归引入方法.B import func_2

@component(output_component_file='func_3_component.yaml', packages_to_install=['joblib', 'resource'])
def func_3(func_3_output:Output[Dataset]):
    from resource.递归引入方法.B import func_2
    import joblib

    def func_2(a):

        def func_1(a, b):
            return (a + b)
        res = func_1(1, a)
        return res
    res = func_2(1)
    joblib.dump({'res': res}, func_3_output.path)

@component(output_component_file='func_4_component.yaml', packages_to_install=['joblib', 'resource'])
def func_4(func_4_output:Output[Dataset]):
    """

    :param func_4_output:
    :return:
    """
    from resource.递归引入方法.B import func_2
    import joblib

    def func_2(a):

        def func_1(a, b):
            return (a + b)
        res = func_1(1, a)
        return res

    def func_3():

        def func_2(a):

            def func_1(a, b):
                return (a + b)
            res = func_1(1, a)
            return res
        res = func_2(1)
        return res
    res = func_2(1)
    res = func_3(1)
    res = func_2(1)
    joblib.dump({'res': res}, func_4_output.path)
