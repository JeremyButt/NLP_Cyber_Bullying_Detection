import re
from spellcheck import spellcheck

class ngramParser(object):

    def __init__(self):
        self.good_word_list = []
        self.bad_word_list = []
        self.second_person_word_list = []
        self.third_person_word_list = []
        self.get_word_lists()
        self.regex = re.compile('[^a-zA-Z]')
        self.lookalikes = {
            "$" : "S",
            "@" : "A",
            "!" : "I",
            "0" : "O",
            "5" : "S",
            "3" : "E",
            "1" : "L",
        }

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
    
    def replaceLetterLookalikes(self, word):
        for lookalike in self.lookalikes:
            word = word.replace(lookalike, self.lookalikes[lookalike])
        return word

    def removeLetterDuplicates(self, word):
        new_word = ""
        i = 0
        while i+2 < len(word):
            next_next = word[i+2]
            next = word[i+1]
            current = word[i]
            if current == next and next == next_next:
                i += 2
                while i < len(word) and word[i] == next:
                    i += 1
                new_word += current
                continue
            new_word += current
            i += 1
        while i < len(word):
            new_word += word[i]
            i += 1
        return new_word

    def get_ngrams(self, text):
        good_words = 0 
        bad_words = 0
        second_person_words = 0
        third_person_words = 0

        words = text.split()
        numWords = len(words) if len(words) != 0 else 1

        for word in words:

            word = self.removeLetterDuplicates(word)
            if len(word) > 15:
                continue

            word = self.replaceLetterLookalikes(word)
            word = self.regex.sub('', word)
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
                 "Good"             :   good_words            / numWords, 
                 "Bad"              :   bad_words             / numWords, 
                 "Second-Person"    :   second_person_words   / numWords, 
                 "Third-Person"     :   third_person_words    / numWords,
                }
