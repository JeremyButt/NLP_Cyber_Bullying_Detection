from autocorrect import spell
from NLP.spellingCache import cache


def spellcheck(word):
    """
    A wrapper function for the autocorrect spelling correction function.
    This caches results to speed up the training process. Autocorrect was used,
    despite being slow, because it has the desired functionality of correcting
    words to swear words. 
    """
    if word in cache:
        return cache[word]
    elif len(word) > 15:
        return ""
    else:
        spellchecked_word = spell(word)
        cache[word] = spellchecked_word
        return spellchecked_word

def exportCache():
    """
    Store results in dictionary.
    """
    with open("spellingCache.py", 'w+') as f:
        f.truncate()
        f.write("cache = {\n")
        for word in cache:
            f.write('"' + word + '" : "' + cache[word] + '",\n')
        f.write('}\n')
