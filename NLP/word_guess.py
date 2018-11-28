import re

from NLP.spellcheck import spellcheck, exportCache

class WordGuess(object):
    """
    Guess a word given a (possibly greatly misspelled) word.
    """

    def __init__(self):
        self.regex = re.compile('[^a-zA-Z]')
        # Common letter lookalikes used in text-talk.
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

    def guess(self, word):
        """
        Return the best-guess for a given word.
        """
        word = self.removeLetterDuplicates(word)
        word = self.replaceLetterLookalikes(word)
        word = self.regex.sub('', word)
        word = spellcheck(word.lower())
        return word
    
    def cache(self):
        """
        Cache the spelling correction results for the word.
        """
        exportCache()
