import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp

from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
import joblib

@component(output_component_file='load_digits_component.yaml', packages_to_install=['sklearn.model_selection', 'joblib', 'sklearn'])
def load_digits(load_digits_input:Input[Dataset], load_digits_output:Output[Dataset]):
    import joblib
    from sklearn import datasets, svm, metrics
    from sklearn.model_selection import train_test_split
    import joblib
    load_digits = joblib.load(load_digits_input.path)['load_digits']
    digits = datasets.load_digits()
    return joblib.dump({'digits': digits}, load_digits_output.path)

@component(output_component_file='SVM_component.yaml', packages_to_install=['sklearn.model_selection', 'joblib', 'sklearn'])
def SVM(gamma_input:Input[Dataset], SVM_output:Output[Dataset]):
    import joblib
    from sklearn import datasets, svm, metrics
    from sklearn.model_selection import train_test_split
    import joblib
    gamma = joblib.load(gamma_input.path)['gamma']
    classifier = svm.SVC(gamma=gamma)
    return joblib.dump({'classifier': classifier}, SVM_output.path)

@component(output_component_file='train_test_split_component.yaml', packages_to_install=['sklearn.model_selection', 'joblib', 'sklearn'])
def train_test_split(data_input:Input[Dataset], digits_input:Input[Dataset], test_size_input:Input[Dataset], shuffle_input:Input[Dataset], train_test_split_output:Output[Dataset]):
    import joblib
    from sklearn import datasets, svm, metrics
    from sklearn.model_selection import train_test_split
    import joblib
    data = joblib.load(data_input.path)['data']
    digits = joblib.load(digits_input.path)['digits']
    test_size = joblib.load(test_size_input.path)['test_size']
    shuffle = joblib.load(shuffle_input.path)['shuffle']
    (X_train, X_test, y_train, y_test) = train_test_split(data, digits.target, test_size=test_size, shuffle=shuffle)
    res = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}
    return joblib.dump({'res': res}, train_test_split_output.path)

@component(output_component_file='digitsReshape_component.yaml', packages_to_install=['sklearn.model_selection', 'joblib', 'sklearn'])
def digitsReshape(digits_input:Input[Dataset], digitsReshape_output:Output[Dataset]):
    import joblib
    from sklearn import datasets, svm, metrics
    from sklearn.model_selection import train_test_split
    import joblib
    digits = joblib.load(digits_input.path)['digits']
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, (- 1)))
    return joblib.dump({'data': data}, digitsReshape_output.path)

@component(output_component_file='classfierFit_component.yaml', packages_to_install=['sklearn.model_selection', 'joblib', 'sklearn'])
def classfierFit(split_res_input:Input[Dataset], classifier_input:Input[Dataset], classfierFit_output:Output[Dataset]):
    import joblib
    from sklearn import datasets, svm, metrics
    from sklearn.model_selection import train_test_split
    import joblib
    split_res = joblib.load(split_res_input.path)['split_res']
    classifier = joblib.load(classifier_input.path)['classifier']
    classifier.fit(split_res['X_train'], split_res['y_train'])
    return joblib.dump({'classifier': classifier}, classfierFit_output.path)

@component(output_component_file='classifierPredict_component.yaml', packages_to_install=['sklearn.model_selection', 'joblib', 'sklearn'])
def classifierPredict(split_res_input:Input[Dataset], classifier_input:Input[Dataset], classifierPredict_output:Output[Dataset]):
    import joblib
    from sklearn import datasets, svm, metrics
    from sklearn.model_selection import train_test_split
    import joblib
    split_res = joblib.load(split_res_input.path)['split_res']
    classifier = joblib.load(classifier_input.path)['classifier']
    predicted = classifier.predict(split_res['X_test'])
    print(('Classification report for classifier %s:\n%s\n' % (classifier, metrics.classification_report(split_res['y_test'], predicted))))
    return joblib.dump({'predicted': predicted}, classifierPredict_output.path)
