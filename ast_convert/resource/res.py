import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp

import multiprocessing
from typing import Any, Dict, List, Optional, Tuple, Union
from ConfigSpace import Configuration
import numpy as np
__all__ = ['eval_t', 'TestEvaluator']

@component(output_component_file='eval_t_component.yaml', packages_to_install=['joblib', 'multiprocessing', 'ConfigSpace', 'numpy', 'typing'])
def eval_t(queue_input:Input[Dataset], config_input:Input[Dataset], backend_input:Input[Dataset], metric_input:Input[Dataset], seed_input:Input[Dataset], num_run_input:Input[Dataset], instance_input:Input[Dataset], scoring_functions_input:Input[Dataset], output_y_hat_optimization_input:Input[Dataset], include_input:Input[Dataset], exclude_input:Input[Dataset], disable_file_output_input:Input[Dataset], port_input:Input[Dataset], additional_components_input:Input[Dataset], init_params_input:Input[Dataset], budget_input:Input[Dataset], budget_type_input:Input[Dataset], eval_t_output:Output[Dataset]) -> None:
    import multiprocessing
    from ConfigSpace import Configuration
    import numpy as np
    from typing import Any, Dict, List, Optional, Tuple, Union
    import joblib
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
