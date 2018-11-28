from math import log10
from pattern3.en import lemma

from NLP.word_guess import WordGuess
from NLP.ngrams import ngramParser
from NLP.spellcheck import spellcheck
from NLP.tfidfCache import tfidf_cache

# Note: TF-IDF = term frequency - inverse document frequency

class TFIDF(object):
    """
    This class uses TF-IDF scores to determine the severity of the language
    in a message. It looks at only bad word frequencies and uses non-bullying
    messages to find the baseline IDF scores. This method worked best in testing,
    as compared with using good words as well as bad words, or using all messages,
    bullying and non-bullying, to get the basline IDF scores.
    """

    def __init__(self):
        self.guesser = WordGuess()
        self.IDFs = tfidf_cache
        # No need to compute IDFs when using cached data
        # self.compute_IDFs()
        self.ngrams = ngramParser()

    def compute_IDFs(self):
        """
        Compute the IDF scores of each word in the Formspring data.
        """
        comments = []
        with open('../data/DataReleaseDec2011/formspring_data_severity_gt2_5.csv', 'r') as file:
            lines = file.readlines()[1:]
            for line in lines:
                if ',' in line:
                    # Use only the non-bullying cases for the baseline data.
                    # Testing found this provided an improvement.
                    if "False" in line.split(',')[1]:
                        comments.append(line.split(',')[0])

            for comment in comments:
                for word in set(comment.split()):
                    # Use the best guess for the word, instead of the raw word.
                    word = lemma(self.guesser.guess(word))
                    if word in self.IDFs:    
                        self.IDFs[word] += 1
                    else:
                        self.IDFs[word] = 1
            # cache word-guess results
            self.guesser.cache()
            
            for word in self.IDFs:
                # TF-IDF formula: TF-IDF = TF * log(N/n)
                # TF = term frequency of word
                # N = number of total messages in Formspring
                # n = number of messages containing the word
                # Just calculating IDF here so no TF factor.
                self.IDFs[word] =  log10(len(comments) / float(self.IDFs[word]))
                tfidf_cache[word] = self.IDFs[word]
    
    def get_score(self, text):
        """
        Get the TF-IDF score for a message in terms of bad words in the message.
        This was found to be the best indicator in testing.
        """
        score = 0
        for word in text.split():
            word = lemma(self.guesser.guess(word)).lower()
            ngram = self.ngrams.get_ngrams(word)
            score -= ngram["Bad"]*(self.IDFs[word] if word in self.IDFs else 5.0)
        return score

    def cacheScores(self):
        """
        Cache previously-calculated TF-IDF scores and store them in a dictionary.
        """
        with open("tfidfCache.py", 'w+') as f:
            f.truncate()
            f.write("tfidf_cache = {\n")
            for word in tfidf_cache:
                f.write('"' + word + '" : ' + str(tfidf_cache[word]) + ',\n')
            f.write('}\n')
