import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model, InputPath
import kfp.components as comp

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


@component(output_component_file='get_all_datas_component.yaml', packages_to_install=['joblib', 'numpy', 'sklearn'])
def get_all_datas(get_all_datas_output: Output[Dataset]):
    from sklearn.datasets import make_moons, make_circles, make_classification
    from sklearn.neighbors import KNeighborsClassifier
    import numpy as np
    from sklearn.naive_bayes import GaussianNB
    from sklearn.gaussian_process.kernels import RBF
    from sklearn.preprocessing import StandardScaler
    from sklearn.neural_network import MLPClassifier
    from sklearn.gaussian_process import GaussianProcessClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
    from sklearn.svm import SVC
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    from sklearn.tree import DecisionTreeClassifier
    import joblib
    names = ['Nearest Neighbors', 'Linear SVM', 'RBF SVM', 'Gaussian Process', 'Decision Tree', 'Random Forest',
             'Neural Net', 'AdaBoost', 'Naive Bayes', 'QDA']
    classifiers = [KNeighborsClassifier(3), SVC(kernel='linear', C=0.025), SVC(gamma=2, C=1),
                   GaussianProcessClassifier((1.0 * RBF(1.0))), DecisionTreeClassifier(max_depth=5),
                   RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
                   MLPClassifier(alpha=1, max_iter=1000), AdaBoostClassifier(), GaussianNB(),
                   QuadraticDiscriminantAnalysis()]
    linearly_separable = (X, y)
    datasets = [make_moons(noise=0.3, random_state=0), make_circles(noise=0.2, factor=0.5, random_state=1),
                linearly_separable]
    joblib.dump({'names': names, ' classifiers': classifiers, ' datasets': datasets}, get_all_datas_output.path)


@component(output_component_file='make_classification_com_component.yaml',
           packages_to_install=['joblib', 'numpy', 'sklearn'])
def make_classification_com(make_classification_com_output: Output[Dataset]):
    from sklearn.datasets import make_classification
    import joblib
    (X, y) = make_classification(n_features=2, n_redundant=0, n_informative=2, random_state=1, n_clusters_per_class=1)
    joblib.dump({'X': X, ' y': y}, make_classification_com_output.path)


@component(output_component_file='np_random_random_state_component.yaml',
           packages_to_install=['joblib', 'numpy', 'sklearn'])
def np_random_random_state(np_random_random_state_output: Output[Dataset]):
    from sklearn.datasets import make_moons, make_circles, make_classification
    from sklearn.neighbors import KNeighborsClassifier
    import numpy as np
    from sklearn.naive_bayes import GaussianNB
    from sklearn.gaussian_process.kernels import RBF
    from sklearn.preprocessing import StandardScaler
    from sklearn.neural_network import MLPClassifier
    from sklearn.gaussian_process import GaussianProcessClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
    from sklearn.svm import SVC
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    from sklearn.tree import DecisionTreeClassifier
    import joblib
    rng = np.random.RandomState(2)
    joblib.dump({'rng': rng}, np_random_random_state_output.path)


@component(output_component_file='rng_uniform_component.yaml', packages_to_install=['joblib', 'numpy', 'sklearn'])
def rng_uniform(X_input: Input[Dataset], rng_uniform_output: Output[Dataset]):
    from sklearn.datasets import make_moons, make_circles, make_classification
    from sklearn.neighbors import KNeighborsClassifier
    import numpy as np
    from sklearn.naive_bayes import GaussianNB
    from sklearn.gaussian_process.kernels import RBF
    from sklearn.preprocessing import StandardScaler
    from sklearn.neural_network import MLPClassifier
    from sklearn.gaussian_process import GaussianProcessClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
    from sklearn.svm import SVC
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    from sklearn.tree import DecisionTreeClassifier
    import joblib
    X = joblib.load(X_input.path)['X']
    X += (2 * rng.uniform(size=X.shape))
    joblib.dump({'X': X}, rng_uniform_output.path)
