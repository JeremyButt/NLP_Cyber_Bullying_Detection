from sklearn.externals import joblib
from sklearn import svm

from NLP.feature_vector import FeatureVectorGenerator


class Predictor(object):

    def __init__(self, clf=svm.LinearSVC(), model_file='../models/demo_model_tfidf1.joblib'):
        """
        Construct a predictor object with a svm type and a trained model in the form of a joblib file.
        :param clf: a sklearn SVM type
        :param model_file: a valid trained model in the form of a joblib file
        """
        self.feature_vector_generator = FeatureVectorGenerator()
        self.clf = clf
        try:
            self.clf = joblib.load(model_file)
        except FileNotFoundError:
            print('Not a valid model file!')

    def predict(self, string):
        """
        Make a prediction based on a given string
        :param string: potential bullying string
        :return: prediction: the predictions if the string is cyber bullying or not.
        """
        features = self.feature_vector_generator.getFeatureVector(string)
        prediction = (self.clf.predict([features])[0] == 1)
        return prediction
