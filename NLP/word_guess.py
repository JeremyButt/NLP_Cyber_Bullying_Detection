import re

from spellcheck import spellcheck, exportCache

class WordGuess(object):

    def __init__(self):
        self.regex = re.compile('[^a-zA-Z]')
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

    def guess(self, word):
            word = self.removeLetterDuplicates(word)
            word = self.replaceLetterLookalikes(word)
            word = self.regex.sub('', word)
            #word = spellcheck(word.lower())
            return word
    
    def cache(self):
        exportCache()
