#!/usr/bin/python
# -*- coding: utf-8 -*-

from pickle import load
from collections import namedtuple
from textblob import TextBlob
from feature_data import FeatureData


spam_classifier = load(open('classifiers/spam/spam_classifer.pickle'))
topic_classifier = load(open('classifiers/topic/topic_classifier.pickle'))

ProcessedMessage = namedtuple('ProcessedMessage',
                              ['spam', 'ontopic', 'sentiment', 'keywords'],
                              verbose=True)


class Classifier(object):

    def process(self, string):
        return ProcessedMessage(spam=self.get_spam_likelihood(string),
                                ontopic=self.get_ontopic_likelihood(string),
                                sentiment=self.get_sentiment(string),
                                keywords=self.get_keywords(string))

    @staticmethod
    def get_keywords(string):
        txt = TextBlob(string)
        return list(txt.noun_phrases)

    @staticmethod
    def get_sentiment(string):
        txt = TextBlob(string)
        return list(txt.sentiment)

    @staticmethod
    def get_spam_likelihood(string):
        txt = FeatureData(string)
        return spam_classifier.predict(txt.get_features())

    @staticmethod
    def get_ontopic_likelihood(string):
        return topic_classifier.predict([string])


if __name__ == "__main__":
    clf = Classifier()
    t = clf.process("""Return a reader object which will iterate over lines in the
                given csvfile. csvfile can be any object which supports the
                iterator protocol and returns a string each time its next()
                method is called - file objects and list objects are both
                suitable. If csvfile is a file object, it must be opened
                with the `b` flag on platforms where that makes a difference.
                An optional dialect parameter can be given which is used to
                define a set of parameters specific to a particular CSV dialect
                """)
    print(t)
