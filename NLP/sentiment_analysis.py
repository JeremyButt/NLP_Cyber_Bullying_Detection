from monkeylearn import MonkeyLearn

def classify_sentiment(text):
    ml = MonkeyLearn('41cf376565f33670246c5463bb7c34bf5f503969')
    data = [text]
    model_id = 'cl_pi3C7JiL'
    result = ml.classifiers.classify(model_id, data)
    if result.body[0]['classifications'][0]['tag_name'] == 'Positive':
        return (result.body[0]['classifications'][0]['confidence'])
    elif result.body[0]['classifications'][0]['tag_name'] == 'Negative':
        return -(result.body[0]['classifications'][0]['confidence'])

