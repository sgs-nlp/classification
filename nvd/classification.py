import pickle
import pandas
import glob
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn import svm as support_vector_machine
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression as sklearn_lr
from sklearn.metrics import (
    accuracy_score as sk_learn_accuracy_score,
    f1_score as sk_learn_f1_score,
    precision_score as sk_learn_precision_score,
    recall_score as sk_learn_recall_score,
)

from nvd.normalizer import matrix_scale_matrix
from nvd.embedding import GDoc2Vec, BOWDoc2vec, OneHotDoc2vec
from nvd.measure import true_or_false, precision, recall, accuracy


class Classification:
    def __init__(self, x_data, y_data, categories_list):
        self.x_data = x_data
        self.y_data = y_data
        self.categories_list = categories_list

    _x_train = None
    _x_test = None
    _y_train = None
    _y_test = None

    @property
    def x_train(self):
        if self._x_train is not None:
            return self._x_train
        self._x_train, self._x_test, self._y_train, self._y_test = train_test_split(self.x_data, self.y_data,
                                                                                    test_size=0.15, random_state=42)
        return self._x_train

    @property
    def x_test(self):
        if self._x_test is not None:
            return self._x_test
        self._x_train, self._x_test, self._y_train, self._y_test = train_test_split(self.x_data, self.y_data,
                                                                                    test_size=0.15, random_state=42)
        return self._x_test

    @property
    def y_train(self):
        if self._y_train is not None:
            return self._y_train
        self._x_train, self._x_test, self._y_train, self._y_test = train_test_split(self.x_data, self.y_data,
                                                                                    test_size=0.15, random_state=42)
        return self._y_train

    @property
    def y_test(self):
        if self._y_test is not None:
            return self._y_test
        self._x_train, self._x_test, self._y_train, self._y_test = train_test_split(self.x_data, self.y_data,
                                                                                    test_size=0.15, random_state=42)
        return self._y_test

    _svm = None

    @property
    def svm(self):
        if self._svm is not None:
            return self._svm
        self._svm = SVM(self.x_train, self.x_test, self.y_train, self.y_test, self.categories_list)
        return self._svm

    _mlp = None

    @property
    def mlp(self):
        if self._mlp is not None:
            return self._mlp
        self._mlp = MLP(self.x_train, self.x_test, self.y_train, self.y_test, self.categories_list)
        return self._mlp

    _mnb = None

    @property
    def mnb(self):
        if self._mnb is not None:
            return self._mnb
        self._mnb = MNB(self.x_train, self.x_test, self.y_train, self.y_test, self.categories_list)
        return self._mnb

    _lr = None

    @property
    def lr(self):
        if self._lr is not None:
            return self._lr
        self._lr = LogisticRegression(self.x_train, self.x_test, self.y_train, self.y_test, self.categories_list)
        return self._lr

    def create_all(self):
        if self._x_train is None:
            tmp = self.x_train

        if self._x_test is None:
            tmp = self.x_test

        if self._y_train is None:
            tmp = self.y_train

        if self._y_test is None:
            tmp = self.y_test

        if self._svm is None:
            tmp = self.svm

        if self._mlp is None:
            tmp = self.mlp

        if self._mnb is None:
            tmp = self.mnb

        if self._lr is None:
            tmp = self.lr


class SVM:
    def __init__(self, x_train, x_test, y_train, y_test, categories_list):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.categories_list = categories_list

    @property
    def name(self):
        return 'Support Vector Machine'

    _model = None

    @property
    def model(self):
        if self._model is not None:
            return self._model
        self._model = support_vector_machine.LinearSVC()
        self._model.fit(self.x_train, self.y_train)
        return self._model

    _fns = None
    _tps = None
    _tns = None
    _fps = None
    _predicted = None

    @property
    def predicted(self):
        if self._predicted is not None:
            return self._predicted
        self._predicted = self.model.predict(self.x_test)
        return self._predicted

    @property
    def fns(self):
        if self._fns is not None:
            return self._fns
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._fns

    @property
    def tps(self):
        if self._tps is not None:
            return self._tps
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._tps

    @property
    def tns(self):
        if self._tns is not None:
            return self._tns
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._tns

    @property
    def fps(self):
        if self._fps is not None:
            return self._fps
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._fps

    _precision_score = None

    @property
    def precision_score(self):
        if self._precision_score is not None:
            return self._precision_score
        self._precision_score = precision(true_positives=self.tps, false_positives=self.fps)
        return self._precision_score

    _recall_score = None

    @property
    def recall_score(self):
        if self._recall_score is not None:
            return self._recall_score
        self._recall_score = recall(false_negatives=self.fns, true_positives=self.tps)
        return self._recall_score

    _accuracy_score = None

    @property
    def accuracy_score(self):
        if self._accuracy_score is not None:
            return self._accuracy_score
        self._accuracy_score = accuracy(false_negatives=self.fns, true_positives=self.tps, true_negatives=self.tns,
                                        false_positives=self.fps)
        return self._accuracy_score


class MLP:
    def __init__(self, x_train, x_test, y_train, y_test, categories_list):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.categories_list = categories_list

    @property
    def name(self):
        return 'Multi Layer Perceptron'

    _model = None

    @property
    def model(self):
        if self._model is not None:
            return self._model
        self._model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
        self._model.fit(self.x_train, self.y_train)
        return self._model

    _fns = None
    _tps = None
    _tns = None
    _fps = None
    _predicted = None

    @property
    def predicted(self):
        if self._predicted is not None:
            return self._predicted
        self._predicted = self.model.predict(self.x_test)
        return self._predicted

    @property
    def fns(self):
        if self._fns is not None:
            return self._fns
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._fns

    @property
    def tps(self):
        if self._tps is not None:
            return self._tps
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._tps

    @property
    def tns(self):
        if self._tns is not None:
            return self._tns
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._tns

    @property
    def fps(self):
        if self._fps is not None:
            return self._fps
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._fps

    _precision_score = None

    @property
    def precision_score(self):
        if self._precision_score is not None:
            return self._precision_score
        self._precision_score = precision(true_positives=self.tps, false_positives=self.fps)
        return self._precision_score

    _recall_score = None

    @property
    def recall_score(self):
        if self._recall_score is not None:
            return self._recall_score
        self._recall_score = recall(false_negatives=self.fns, true_positives=self.tps)
        return self._recall_score

    _accuracy_score = None

    @property
    def accuracy_score(self):
        if self._accuracy_score is not None:
            return self._accuracy_score
        self._accuracy_score = accuracy(false_negatives=self.fns, true_positives=self.tps, true_negatives=self.tns,
                                        false_positives=self.fps)
        return self._accuracy_score


class MNB:
    def __init__(self, x_train, x_test, y_train, y_test, categories_list):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.categories_list = categories_list

    @property
    def name(self):
        return 'Multinomial Naive Baise'

    _model = None

    @property
    def model(self):
        if self._model is not None:
            return self._model
        self._model = MultinomialNB()
        self._model.fit(self.x_train, self.y_train)
        return self._model

    _fns = None
    _tps = None
    _tns = None
    _fps = None
    _predicted = None

    @property
    def predicted(self):
        if self._predicted is not None:
            return self._predicted
        self._predicted = self.model.predict(self.x_test)
        return self._predicted

    @property
    def fns(self):
        if self._fns is not None:
            return self._fns
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._fns

    @property
    def tps(self):
        if self._tps is not None:
            return self._tps
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._tps

    @property
    def tns(self):
        if self._tns is not None:
            return self._tns
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._tns

    @property
    def fps(self):
        if self._fps is not None:
            return self._fps
        self._fns, self._tps, self._tns, self._fps = true_or_false(self.predicted, self.y_test, self.categories_list)
        return self._fps

    _precision_score = None

    @property
    def precision_score(self):
        if self._precision_score is not None:
            return self._precision_score
        self._precision_score = precision(true_positives=self.tps, false_positives=self.fps)
        return self._precision_score

    _recall_score = None

    @property
    def recall_score(self):
        if self._recall_score is not None:
            return self._recall_score
        self._recall_score = recall(false_negatives=self.fns, true_positives=self.tps)
        return self._recall_score

    _accuracy_score = None

    @property
    def accuracy_score(self):
        if self._accuracy_score is not None:
            return self._accuracy_score
        self._accuracy_score = accuracy(false_negatives=self.fns, true_positives=self.tps, true_negatives=self.tns,
                                        false_positives=self.fps)
        return self._accuracy_score
