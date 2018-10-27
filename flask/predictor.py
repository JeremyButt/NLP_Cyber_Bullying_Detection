import NLP.ngrams as ngrams


def predict(text):
    parser = ngrams.ngramParser()
    vector = parser.get_ngrams(text)
    bullying = vector['Bad'] > vector['Good']

    return bullying
