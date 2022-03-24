from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split


import joblib


def load_digits(load_digits: OutputPath(Dataset)):
    digits = datasets.load_digits()
    return digits


def SVM(gamma):
    classifier = svm.SVC(gamma=gamma)
    return classifier


def train_test_split(data, digits, test_size, shuffle):
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=test_size, shuffle=shuffle)
    res = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }
    return res


def digitsReshape(digits):
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))
    return data


def classfierFit(split_res, classifier):
    classifier.fit(split_res['X_train'], split_res['y_train'])
    return classifier


def classifierPredict(split_res, classifier):
    predicted = classifier.predict(split_res['X_test'])
    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(split_res['y_test'], predicted)))
    return predicted
