import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp

import multiprocessing
from typing import Any, Dict, List, Optional, Tuple, Union
from ConfigSpace import Configuration
import numpy as np
__all__ = ['eval_t', 'TestEvaluator']

@component(output_component_file='eval_t_component.yaml', packages_to_install=['numpy', 'typing', 'joblib', 'ConfigSpace', 'multiprocessing'])
def eval_t(queue_input:Input[Dataset], config_input:Input[Dataset], backend_input:Input[Dataset], metric_input:Input[Dataset], seed_input:Input[Dataset], num_run_input:Input[Dataset], instance_input:Input[Dataset], scoring_functions_input:Input[Dataset], output_y_hat_optimization_input:Input[Dataset], include_input:Input[Dataset], exclude_input:Input[Dataset], disable_file_output_input:Input[Dataset], port_input:Input[Dataset], additional_components_input:Input[Dataset], init_params_input:Input[Dataset], budget_input:Input[Dataset], budget_type_input:Input[Dataset], eval_t_output:Output[Dataset]) -> None:
    from typing import Any, Dict, List, Optional, Tuple, Union
    import multiprocessing
    import numpy as np
    from ConfigSpace import Configuration
    import joblib

    class TestEvaluator(AbstractEvaluator):

        def __init__(self, backend: Backend, queue: multiprocessing.Queue, metric: Scorer, additional_components: Dict[(str, ThirdPartyComponents)], port: Optional[int], configuration: Optional[Union[(int, Configuration)]]=None, scoring_functions: Optional[List[Scorer]]=None, seed: int=1, include: Optional[List[str]]=None, exclude: Optional[List[str]]=None, disable_file_output: bool=False, init_params: Optional[Dict[(str, Any)]]=None):
            super(TestEvaluator, self).__init__(backend=backend, queue=queue, port=port, configuration=configuration, metric=metric, additional_components=additional_components, scoring_functions=scoring_functions, seed=seed, output_y_hat_optimization=False, num_run=(- 1), include=include, exclude=exclude, disable_file_output=disable_file_output, init_params=init_params)
            self.configuration = configuration
            self.X_train = self.datamanager.data['X_train']
            self.Y_train = self.datamanager.data['Y_train']
            self.X_test = self.datamanager.data.get('X_test')
            self.Y_test = self.datamanager.data.get('Y_test')
            self.model = self._get_model()

        def fit_predict_and_loss(self) -> None:
            _fit_and_suppress_warnings(self.logger, self.model, self.X_train, self.Y_train)
            (loss, Y_pred, _, _) = self.predict_and_loss()
            self.finish_up(loss=loss, train_loss=None, opt_pred=Y_pred, valid_pred=None, test_pred=None, file_output=False, final_call=True, additional_run_info=None, status=StatusType.SUCCESS)

        def predict_and_loss(self, train: bool=False) -> Tuple[(Union[(Dict[(str, float)], float)], np.array, Any, Any)]:
            if train:
                Y_pred = self.predict_function(self.X_train, self.model, self.task_type, self.Y_train)
                err = calculate_loss(solution=self.Y_train, prediction=Y_pred, task_type=self.task_type, metric=self.metric, scoring_functions=self.scoring_functions)
            else:
                Y_pred = self.predict_function(self.X_test, self.model, self.task_type, self.Y_train)
                err = calculate_loss(solution=self.Y_test, prediction=Y_pred, task_type=self.task_type, metric=self.metric, scoring_functions=self.scoring_functions)
            return (err, Y_pred, None, None)
    queue = joblib.load(queue_input.path)['queue']
    config = joblib.load(config_input.path)['config']
    backend = joblib.load(backend_input.path)['backend']
    metric = joblib.load(metric_input.path)['metric']
    seed = joblib.load(seed_input.path)['seed']
    num_run = joblib.load(num_run_input.path)['num_run']
    instance = joblib.load(instance_input.path)['instance']
    scoring_functions = joblib.load(scoring_functions_input.path)['scoring_functions']
    output_y_hat_optimization = joblib.load(output_y_hat_optimization_input.path)['output_y_hat_optimization']
    include = joblib.load(include_input.path)['include']
    exclude = joblib.load(exclude_input.path)['exclude']
    disable_file_output = joblib.load(disable_file_output_input.path)['disable_file_output']
    port = joblib.load(port_input.path)['port']
    additional_components = joblib.load(additional_components_input.path)['additional_components']
    init_params = joblib.load(init_params_input.path)['init_params']
    budget = joblib.load(budget_input.path)['budget']
    budget_type = joblib.load(budget_type_input.path)['budget_type']
    evaluator = TestEvaluator(configuration=config, backend=backend, metric=metric, seed=seed, port=port, queue=queue, scoring_functions=scoring_functions, include=include, exclude=exclude, disable_file_output=disable_file_output, additional_components=additional_components, init_params=init_params)
    evaluator.fit_predict_and_loss()
