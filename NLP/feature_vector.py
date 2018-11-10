from pattern3.en import sentiment
import numpy as np

from NLP.ngrams import ngramParser
from NLP.spellcheck import exportCache
from NLP.sentenceParser import SentenceParser

class FeatureVectorGenerator(object):

    def __init__(self):
        self.parser = ngramParser()
        self.sentence_parser = SentenceParser()
    
    def cache(self):
        self.sentence_parser.cacheScores()
        exportCache()

    def getFeatureVector(self, text):

        ngram_vector = self.parser.get_ngrams(text)
        sentiment_values = sentiment(text)
        sentiment_score = sentiment_values[0]
        sentiment_objectivity = sentiment_values[1]
        sentence_score = self.sentence_parser.parseSentences(text)

        vector =    [
                        (ngram_vector["Good"]-ngram_vector["Bad"])*(ngram_vector["Second-Person"]),
                        ngram_vector["Bad"],
                        sentence_score,
                        sentiment_score*sentiment_objectivity,
                        ngram_vector["Second-Person"],
                    ]
        return np.array(vector).astype(float)
