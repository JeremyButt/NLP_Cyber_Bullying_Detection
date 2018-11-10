import spacy
from pattern3.en import sentiment

from NLP.ngrams import ngramParser
from NLP.sentenceCache import cache

class SentenceParser(object):
    
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.second_person_word_list = []
        self.ngram_parser = ngramParser()
        with open("./data/second_person_pronoun.dict", 'r') as file:
            self.second_person_word_list = file.read().replace('\n', ' ').split()
    
    def parseSentences(self, text):
        if text.replace('"', '') in cache:
            return cache[text.replace('"', '')]

        tokens = self.nlp(text)
        sentences = tokens.sents
        numSentences = 0
        score = 0

        for sentence in sentences:
            numSentences += 1
            ngram_vector = self.ngram_parser.get_ngrams(sentence.text)
            if ngram_vector["Second-Person"] > 0:
                score -= ngram_vector["Bad"]
                score += ngram_vector["Good"]

        score /= numSentences
        cache[text.replace('"', '')] = score
        return score

    def cacheScores(self):
        with open("./NLP/sentenceCache.py", 'w+') as f:
            f.truncate()
            f.write("cache = {\n")
            for message in cache:
                f.write('"' + message + '" : ' + str(cache[message]) + ',\n')
            f.write('}\n')
