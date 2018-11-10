from math import log10
from pattern3.en import lemma

from NLP.word_guess import WordGuess
from NLP.ngrams import ngramParser
from NLP.spellcheck import spellcheck
from NLP.tfidfCache import tfidf_cache

class TFIDF(object):

    def __init__(self):
        self.guesser = WordGuess()
        self.IDFs = tfidf_cache
        # No need to compute IDFs when using cached data
        #self.compute_IDFs()
        self.ngrams = ngramParser()

    def compute_IDFs(self):
        comments = []
        with open('../data/DataReleaseDec2011/formspring_data_severity_gt2_5.csv', 'r') as file:
            lines = file.readlines()[1:]
            for line in lines:
                if ',' in line:
                    if "False" in line.split(',')[1]:
                        comments.append(line.split(',')[0])

            for comment in comments:
                for word in set(comment.split()):
                    word = lemma(self.guesser.guess(word))
                    if word in self.IDFs:    
                        self.IDFs[word] += 1
                    else:
                        self.IDFs[word] = 1
            self.guesser.cache()
            
            for word in self.IDFs:
                self.IDFs[word] =  log10(len(comments) / float(self.IDFs[word]))
                tfidf_cache[word] = self.IDFs[word]
    
    def get_score(self, text):
        score = 0
        for word in text.split():
            word = lemma(self.guesser.guess(word)).lower()
            ngram = self.ngrams.get_ngrams(word)
            score -= ngram["Bad"]*(self.IDFs[word] if word in self.IDFs else 5.0)
        return score

    def cacheScores(self):
        with open("tfidfCache.py", 'w+') as f:
            f.truncate()
            f.write("tfidf_cache = {\n")
            for word in tfidf_cache:
                f.write('"' + word + '" : ' + str(tfidf_cache[word]) + ',\n')
            f.write('}\n')
