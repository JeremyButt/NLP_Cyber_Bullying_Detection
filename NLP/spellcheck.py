from autocorrect import spell
from spelling_cache import cache

def spellcheck(word):
    if len(word) > 15:
        return ""
    if word in cache:
        return cache[word]
    else:
        spellchecked_word = spell(word)
        cache[word] = spellchecked_word
        return spellchecked_word

def exportCache(filename):
    with open(filename, 'w+') as f:
        f.truncate()
        f.write("cache = {\n")
        for word in cache:
            f.write('"' + word + '" : "' + cache[word] + '",\n')
        f.write('}')
