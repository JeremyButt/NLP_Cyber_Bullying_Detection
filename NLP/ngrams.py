from autocorrect import spell
import re

class ngramParser(object):

    def __init__(self):
        self.good_word_list = []
        self.bad_word_list = []
        self.second_person_word_list = []
        self.third_person_word_list = []
        self.get_word_lists()

    def get_word_lists(self):
        with open("../data/good_words.dict", 'r') as file:
            self.good_word_list = file.read().replace('\n', ' ').split()

        with open("../data/bad_words.dict", 'r') as file:
            self.bad_word_list = file.read().replace('\n', ' ').split()
        
        with open("../data/second_person_pronoun.dict", 'r') as file:
            self.second_person_word_list = file.read().replace('\n', ' ').split()

        with open("../data/third_person_pronoun.dict", 'r') as file:
            self.third_person_word_list = file.read().replace('\n', ' ').split()

    def get_word_emphasis(self, word):
        if word.isupper():
            return 2
        else:
            return 1

    def get_ngrams(self, text):
        good_words = 0 
        bad_words = 0
        second_person_words = 0
        third_person_words = 0

        words = text.split()
        regex = re.compile('[^a-zA-Z]')

        for word in words:

            word = regex.sub('', word)
            word_emphasis = self.get_word_emphasis(word)
            word = word.lower()

            if word in self.good_word_list or spell(word) in self.good_word_list:
                good_words += word_emphasis
            
            if word in self.bad_word_list or spell(word) in self.bad_word_list:
                bad_words += word_emphasis
            
            if word in self.second_person_word_list or spell(word) in self.second_person_word_list:
                second_person_words += word_emphasis
            
            if word in self.third_person_word_list or spell(word) in self.third_person_word_list:
                third_person_words += word_emphasis


        return  {
                 "Good": good_words, 
                 "Bad": bad_words, 
                 "Second-Person": second_person_words, 
                 "Third-person": third_person_words
                }


if __name__ == "__main__":
    parser = ngramParser()
    print(parser.get_ngrams("You, are a MOTHEFUCKER."))
    print(parser.get_ngrams("You, are a nice MOTHEFUCKER."))
