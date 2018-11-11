import sys

from sklearn import svm
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.externals import joblib
import pandas as pd
import numpy as np

from NLP.feature_vector import FeatureVectorGenerator

# Declare Global Defaults
DEFAULT_TRAIN_TO_TEST_RATIO = 0.8
DEFAULT_FEATURE_SOURCE = 'text'
DEFAULT_LABEL_SOURCE = 'label'
DEFAULT_VERBOSE = False


class Trainer(object):

    def __init__(self, clf=svm.LinearSVC(), data_filepath='', train_to_test_ratio=DEFAULT_TRAIN_TO_TEST_RATIO,
                 feature_source=DEFAULT_FEATURE_SOURCE, label_source=DEFAULT_LABEL_SOURCE ,verbose=DEFAULT_VERBOSE):
        """
        Init a Trainer Object
        :param clf: sklearn svm model (default = linearSVC)
        :param data_filepath: filepath to the data in csv form
        :param train_to_test_ratio: ratio of training data points to testing data points
        """
        if data_filepath.split('.')[-1] != 'csv':
            if verbose:
                print('INCORRECT FILE TYPE')
            exit(-1)
        self.data_filepath = data_filepath

        if verbose:
            print('IMPORTING DATA VIA PANDAS READ CSV')
        data_set = pd.read_csv(data_filepath)

        if train_to_test_ratio > 0:
            if verbose:
                print('STRATIFIED SPLITING TRAINING AND TEST DATA')
                train_data, test_data = self.__get_training_and_testing_data(data_set=data_set,
                                                                             train_to_test_ratio=train_to_test_ratio,
                                                                             split_column='label',
                                                                             verbose=verbose)

            if verbose:
                print('GETTING FEATURE VECTORS VIA FEATURE VECTOR GENERATOR')
                print('\tTRAINING DATA')
            self.training_data_feature_vectors, self.training_data_feature_labels = self.__get_data_set_features(data_set=train_data, feature_source=feature_source, label_source=label_source, verbose=verbose)

            if verbose:
                print('\tTESTING DATA')
            self.testing_data_feature_vectors, self.testing_data_feature_labels = self.__get_data_set_features(data_set=test_data, feature_source=feature_source, label_source=label_source, verbose=verbose)

        else:
            if verbose:
                print('GETTING FEATURE VECTORS VIA FEATURE VECTOR GENERATOR')
                print('\tTESTING DATA')
            self.testing_data_feature_vectors, self.testing_data_feature_labels = self.__get_data_set_features(data_set=data_set, feature_source=feature_source, label_source=label_source, verbose=verbose)

        self.clf = clf

        # INIT Predictive stats counts
        self.tp_count = 0
        self.fp_count = 0
        self.tn_count = 0
        self.fn_count = 0

    def train(self, verbose=DEFAULT_VERBOSE):
        """
        Train the model
        :param verbose: if verbose
        :return:
        """
        if verbose:
            print('STARTING TRAINING')

        self.clf.fit(self.training_data_feature_vectors, self.training_data_feature_labels)

    def test(self, verbose=DEFAULT_VERBOSE):
        """
        Test the model
        :param verbose: if verbose
        :return:
        """
        if verbose:
            print('STARTING TESTING')

        for i, feature_vector in enumerate(self.testing_data_feature_vectors):
            prediction = self.clf.predict([feature_vector])
            real = self.testing_data_feature_labels[i]

            if prediction == 0 and real == 0:
                self.tn_count += 1
            elif prediction == 1 and real == 0:
                self.fp_count += 1
            elif prediction == 0 and real == 1:
                self.fn_count += 1
            elif prediction == 1 and real == 1:
                self.tp_count += 1

        if verbose:
            print('DONE TESTING')

    def display_results(self):
        """
        Print out all statistics on the the trained model
        :return:
        """
        print('---------------------------------------')
        print('RESULTS\n')
        print('CONFUSION MATRIX')
        print('n={0}        | Predicted = NO | Predicted = YES'.format(str(self.fp_count + self.tn_count + self.tp_count + self.fn_count)))
        print('Actual = NO  | TN = {0}       | FP = {1}       |{2}'.format(str(self.tn_count), str(self.fp_count), str(self.tn_count + self.fp_count)))
        print('Actual = YES | FN = {0}       | TP = {1}       |{2}'.format(str(self.fn_count), str(self.tp_count), str(self.fn_count + self.tp_count)))
        print('             | {0}            | {1}            |'.format(str(self.tn_count + self.fn_count), str(self.fp_count + self.tp_count)))

        print('\n')

        print('STATISTICS')
        precision = self.tp_count/(self.tp_count + self.fp_count) if (self.tp_count + self.fp_count) != 0 else 0
        recall = self.tp_count/(self.tp_count + self.fn_count) if (self.tp_count + self.fn_count) != 0 else 0
        print('PRECISION: {0}'.format(str(precision)))
        print('RECALL: {0}'.format(str(recall)))

    def save_model(self, file_name='./models/default_model.joblib'):
        """
        Export model to a joblib file
        :param file_name: model file path (always store in .models)
        :return:
        """
        open(file_name, 'w+').close()
        joblib.dump(self.clf, file_name)

    def load_model(self, file_name='./models/default_model.joblib'):
        """
        Import a model file into the clf
        :param file_name: model file path
        :return:
        """
        try:
            self.clf = joblib.load(file_name)
        except FileNotFoundError:
            print('Not a valid model file!')

    @staticmethod
    def __get_training_and_testing_data(data_set=pd.DataFrame, train_to_test_ratio=DEFAULT_TRAIN_TO_TEST_RATIO,
                                        split_column='', verbose=DEFAULT_VERBOSE):
        """
        Using Stratified Shuffle to segment data_set into test and training data_set that properly represent the data.
        :param data_set: Pandas DataFrame with the valid data in it
        :param train_to_test_ratio: ratio of training data points to testing data points
        :param split_column: column create stratified split on
        :return: Training Dataset and Test Dataset
        """
        split = StratifiedShuffleSplit(n_splits=1, test_size=(1-train_to_test_ratio), random_state=42)
        strat_train_set = pd.DataFrame()
        strat_test_set = pd.DataFrame()
        for train_index, test_index in split.split(data_set, data_set[split_column]):
            strat_train_set = data_set.loc[train_index]
            strat_test_set = data_set.loc[test_index]
        return strat_train_set, strat_test_set

    @staticmethod
    def __get_data_set_features(data_set=pd.DataFrame, feature_source=DEFAULT_FEATURE_SOURCE, label_source=DEFAULT_LABEL_SOURCE, verbose=DEFAULT_VERBOSE):
        """
        Get feature vectors for the given dataset
        :param data_set: valid pandas dataframe
        :param feature_source: column name of what should generate the features
        :param label_source:  column name of the label
        :param verbose: if verbose
        :return: feature vectors, labels
        """
        feature_vector_generator = FeatureVectorGenerator()
        features = []
        labels = np.array(list(data_set[label_source].astype(int))).astype(float)
        i = 0
        for index, row in data_set.iterrows():
            if verbose:
                sys.stdout.write('\r\tON INDEX: ' + str(i))
                sys.stdout.flush()
            features.append(feature_vector_generator.getFeatureVector(row[feature_source]))
            i += 1
        print('\n')
        feature_vector_generator.cache()
        return np.array(features).astype(float), labels


# DEMO CODE
if __name__ == '__main__':
    trainer = Trainer(clf=svm.SVC(), data_filepath='./data/DataReleaseDec2011/formspring_data_severity_gt2_5.csv', train_to_test_ratio=0.80,
                 feature_source='text', label_source='label', verbose=True)

    trainer.train(verbose=True)
    trainer.test(verbose=True)
    trainer.display_results()
    trainer.save_model('../models/demo_model.joblib')

    del trainer
    trainer = Trainer(clf=svm.SVC(), data_filepath='./data/DataReleaseDec2011/formspring_data_severity_gt2_5.csv', train_to_test_ratio=0.0,
                 feature_source='text', label_source='label', verbose=True)
    trainer.load_model('../models/demo_model.joblib')
    trainer.test(verbose=True)

    trainer.display_results()
