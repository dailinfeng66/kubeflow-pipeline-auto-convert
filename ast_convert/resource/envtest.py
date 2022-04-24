import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp

@component(output_component_file='make_classification_com_component.yaml', packages_to_install=['joblib', 'numpy','sklearn'])
def make_classification_com(make_classification_com_output:Output[Dataset]):
    from sklearn.datasets import make_moons, make_circles, make_classification
    import numpy as np
    import joblib
    (X, y) = make_classification(n_features=2, n_redundant=0, n_informative=2, random_state=1, n_clusters_per_class=1)
    joblib.dump({'X': X, ' y': y}, make_classification_com_output.path)