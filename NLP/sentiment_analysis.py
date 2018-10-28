from pattern3.en import sentiment

with open("../data/DataReleaseDec2011/formspring_data.csv", 'r') as data:
    with open("../data/DataReleaseDec2011/formspring_data_sentiments.csv", 'w+') as sentiments:
        for line in data.readlines():
            if not line.isspace():
                values = line.split(',')
                values[1] = values[1].replace('\n', '')
                print(values[0])
                sentiment_value = sentiment(values[0])
                sentiments.write(values[0] + ',' + values[1] + ',' + str(sentiment_value[0]) + ',' + str(sentiment_value[1]) + '\n\n')
