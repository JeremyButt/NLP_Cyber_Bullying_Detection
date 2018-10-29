from ngrams import ngramParser
from pattern3.en import sentiment
import numpy as np
from sklearn import svm

import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from spellcheck import exportCache

class FeatureVectorGenerator(object):

    def __init__(self):
        self.parser = ngramParser()

    def getFeatureVector(self, text):

        ngram_vector = self.parser.get_ngrams(text)
        sentiment_values = sentiment(text)
        sentiment_score = sentiment_values[0]
        sentiment_objectivity = sentiment_values[1]

        vector =    [
                        (ngram_vector["Good"]-ngram_vector["Bad"])*ngram_vector["Second-Person"],
                        #ngram_vector["Bad"],
                        #sentiment_score,# * sentiment_objectivity,
                        #ngram_vector["Second-Person"],
                        #ngram_vector["Third-Person"],
                    ]
        return np.array(vector).astype(float)
