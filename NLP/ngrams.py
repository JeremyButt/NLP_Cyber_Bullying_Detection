import re
from NLP.spellcheck import spellcheck


class ngramParser(object):
    """
    This class parses the input text as a bag-of-words, and 
    matches them against the lexicon dict files. Note that 
    while this is called an n-gram parser, it actually only
    uses 1-grams. The intention was to use 2-grams and 3-grams,
    but this was decided against due to previous research showing
    that they are generally less effective.
    """

    def __init__(self):
        self.good_word_list = set()
        self.bad_word_list = set()
        self.second_person_word_list = set()
        self.third_person_word_list = set()
        self.get_word_lists()
        self.regex = re.compile('[^a-zA-Z]')
        # some common character lookalikes used in text-talk.
        self.lookalikes = {
            "$" : "S",
            "@" : "A",
            "!" : "I",
            "0" : "O",
            "5" : "S",
            "3" : "E",
            "1" : "L",
            "(" : "C",
            "+" : "T",
        }

    def get_word_lists(self):
        """
        Convert the word list files into Python lists
        """
        with open("../data/good_words.dict", 'r') as file:
            self.good_word_list = file.read().replace('\n', ' ').split()

        with open("../data/bad_words.dict", 'r') as file:
            self.bad_word_list = file.read().replace('\n', ' ').split()
        
        with open("../data/second_person_pronoun.dict", 'r') as file:
            self.second_person_word_list = file.read().replace('\n', ' ').split()

        with open("../data/third_person_pronoun.dict", 'r') as file:
            self.third_person_word_list = file.read().replace('\n', ' ').split()

    def get_word_emphasis(self, word):
        """
        Add emphasis to words which are all-caps, as they indicate shouting.
        """
        if word.isupper():
            return 2.0
        else:
            return 1.0
    
    def replaceLetterLookalikes(self, word):
        """
        Replace letters with their lookalikes.
        """
        for lookalike in self.lookalikes:
            word = word.replace(lookalike, self.lookalikes[lookalike])
        return word

    def removeLetterDuplicates(self, word):
        """
        Replace strings of three-or-more repeteated letters (e.g. "aaa")
        with a single instance of the letter. Deals with common messaging
        practice of repeating long strings of letters in words.
        """
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
        """
        Use 1-grams to get the frequencies of words from each 
        lexicon dict in the given phrase. 
        """
        good_words = 0 
        bad_words = 0
        second_person_words = 0
        third_person_words = 0

        words = text.split()
        numWords = len(words) if len(words) != 0 else 1

        for word in words:

            word = self.removeLetterDuplicates(word)

            word = self.replaceLetterLookalikes(word)
            word = self.regex.sub('', word)
            word_emphasis = self.get_word_emphasis(word) 
            word = word.lower()
            corrected_word = spellcheck(word).lower()

            # Check the word both with and without spelling correction.
            # This is because spelling correction can sometimes introduce errors.
            possible_words = set()
            possible_words.add(word)
            possible_words.add(corrected_word)
            
            if len(possible_words.intersection(self.bad_word_list)) > 0:
                bad_words += word_emphasis

            if len(possible_words.intersection(self.good_word_list)) > 0:
                good_words += word_emphasis
            
            if len(possible_words.intersection(self.second_person_word_list)) > 0:
                second_person_words += word_emphasis
            
            if len(possible_words.intersection(self.third_person_word_list)) > 0:
                third_person_words += word_emphasis


        return  {
                 "Good"             :   good_words            / numWords, 
                 "Bad"              :   bad_words             / numWords, 
                 "Second-Person"    :   second_person_words   / numWords, 
                 "Third-Person"     :   third_person_words    / numWords, # Note: this is never actually used in the final feature vectors.
                }
