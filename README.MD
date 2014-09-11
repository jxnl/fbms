# Yet Another Spam Detection Attempt (YASDA)

This project is yet another attempt at spam detection. Spawned from conversations on the 
`Hackathon Hackers` facebook page. I will try to develop an automated moderator on facebook
that will use traditional ML techniques to detect and prevent SPAM amoung other things like OffTopic
discussions, Hate Speech and more*. Probably not more. 

#  Data

The first thing we need is data. The datasets I will use to is a bit diverse but I think that 
the assumptions I will make will hold under the conditions that I am trying to detect spam in a
Facebook Discussion group.

My intention is to have a set of serialized training data for the three following topic

One dataset for spam (this will be trained with sys_data and enron_data)
Multiple serlized datasets for each group used for a one vs all classifer

### Exploration

The first step is to collected data from the very active HH group. Save the data then run topic 
detection on it and look at a histogram. If it is fairly sparse, we will go for a PositiveNaiveBayse
off-topic detection. 

### onTopicDetection

http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

Using this tutorial I should be able to train a one versus many classifer.

    groups = List<long>
    for group in groups:
        group_data = data["group"]
        other_data = []
        for other_groups in [g in groups if g != groups]:
            other_data.append(data["other_group"])
        testing, training = split(group_data, other_data)
        classifer['group'] = multinomialNB()
        training = process(training)
        classifer['group'].fit(training)
        results = classifer['group'].train(training)
        logging.print(results)

all we need to do is define a `process` function

### spamDetection

Some features for spam detection using ordinal features. One thing I would like to try is to
train enron and test on sys and vice versa

* countOfURLS
* watchWordsCount
* puntucationRatio
* capitalizedWordCount
* bag of words

    def process(data):
        f1 = countURL(data)
        f2 = punctRatio(data)
        f3 = numberOfSensitiveWords(data)
        f4 = capitalizedWordCount(data)
        f6 = bagOfWords(data)
        return (f1, f2, f3, f4, f5)

Consider using a DictVectorizor for these features

    def process(data):
        features = [countURL, 
                    punctRatio,
                    numberOfSensitiveWords,
                    capitalizedWordCount,
                    bagOfWords,]
        for f in features:
            output[f.__name__]

http://scikit-learn.org/stable/modules/feature_extraction.html

