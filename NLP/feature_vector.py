from ngrams import ngramParser
from pattern3.en import sentiment
from pattern3.en import suggest

import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from spellcheck import exportCache

class FeatureVectorGenerator(object):

    def __init__(self):
        self.parser = ngramParser()

    def getFeatureVector(self, text):

        ngram_vector = self.parser.get_ngrams(text)
        sentiment_values = sentiment(text)
        sentiment_score = sentiment_values[0]
        sentiment_objectivity = sentiment_values[1]

        return  [
                    ngram_vector["Good"],
                    ngram_vector["Bad"],
                    sentiment_score * sentiment_objectivity,
                    ngram_vector["Second-Person"]
                ]

if __name__ == "__main__":
    gen = FeatureVectorGenerator()
    #print(gen.getFeatureVector("FUCK YOU BITCH. I hate you"))

    x = []
    y = []
    z = []
    colours = []

    with open("../data/DataReleaseDec2011/formspring_data.csv", 'r') as data:
        count = 0
        removed = 0
        incorrect = 0
        for line in data.readlines():
            if not line.isspace():
                # if count > 5000:
                #     break
                count += 1
                if count == 1:
                    continue

                values = line.split(',')
                print(count)
                vec = gen.getFeatureVector(values[0])
                xval = 0.0
                if vec[1] == 0:
                    xval = 1.0
                    removed += 1
                    if "True" in values[1]:
                        incorrect += 1
                    continue            
                else:
                    xval = -vec[1]
                x.append(vec[2])
                y.append(vec[0])
                if "True" in values[1]:
                    colours.append('r')
                elif "False" in values[1]:
                    colours.append('b')
    
    #fig = plt.figure()
    #ax = Axes3D(fig)
    #exportCache("spelling_cache.py")
    print("removed "+str(removed))
    print("incorrect: "+str(incorrect))
    plt.scatter(x, y, c=colours)
    plt.show()
