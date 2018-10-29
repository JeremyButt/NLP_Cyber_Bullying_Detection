from autocorrect import spell
from spellingCache import cache

def spellcheck(word):
    if word in cache:
        return cache[word]
    elif len(word) > 15:
        return ""
    else:
        spellchecked_word = spell(word)
        cache[word] = spellchecked_word
        return spellchecked_word

def exportCache():
    with open("spellingCache.py", 'w+') as f:
        f.truncate()
        f.write("cache = {\n")
        for word in cache:
            f.write('"' + word + '" : "' + cache[word] + '",\n')
        f.write('}\n')
