from autocorrect import spell
import re
from spellcheck import spellcheck


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
            return 2.0
        else:
            return 1.0

    def get_ngrams(self, text):
        good_words = 0 
        bad_words = 0
        second_person_words = 0
        third_person_words = 0

        words = text.split()
        numWords = len(words) if len(words) != 0 else 1
        regex = re.compile('[^a-zA-Z]')

        for word in words:
            
            if len(word) > 15:
                continue

            word = regex.sub('', word)
            word_emphasis = self.get_word_emphasis(word)
            word = word.lower()
            corrected_word = spellcheck(word)

            if word in self.good_word_list or corrected_word in self.good_word_list:
                good_words += word_emphasis
            
            if word in self.bad_word_list or corrected_word in self.bad_word_list:
                bad_words += word_emphasis
            
            if word in self.second_person_word_list or corrected_word in self.second_person_word_list:
                second_person_words += word_emphasis
            
            if word in self.third_person_word_list or corrected_word in self.third_person_word_list:
                third_person_words += word_emphasis


        return  {
                 "Good"             : good_words            / numWords, 
                 "Bad"              : bad_words             / numWords, 
                 "Second-Person"    : second_person_words   / numWords, 
                 "Third-person "    : third_person_words    / numWords
                }


if __name__ == "__main__":
    parser = ngramParser()
    print(parser.get_ngrams("Your a bitch"))
    print(parser.get_ngrams("You, are a nice MOTHEFUCKER."))
