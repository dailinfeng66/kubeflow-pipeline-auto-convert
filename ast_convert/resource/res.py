import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp


class Test():

    @component(output_component_file='add_func_component.yaml', packages_to_install=['joblib'])
    def add_func(self_input:Input[Dataset], aaa_input:Input[Dataset], add_func_output:Output[Dataset]):
        import joblib
        self = joblib.load(self_input.path)['self']
        aaa = joblib.load(aaa_input.path)['aaa']
        aaa_ = (aaa + 1)
        return joblib.dump({'aaa_': aaa_}, add_func_output.path)

@component(output_component_file='test_component.yaml', packages_to_install=['joblib'])
def test(ccc_input:Input[Dataset], test_output:Output[Dataset]):
    import joblib
    ccc = joblib.load(ccc_input.path)['ccc']
    test = Test()
    func = test.add_func(ccc)
    return joblib.dump({'func': func}, test_output.path)
