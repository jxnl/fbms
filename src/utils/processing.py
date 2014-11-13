#!/usr/bin/python
# -*- coding: utf-8 -*-

from pickle import load
from feature_data import FeatureData


spam_classifier = load(open('classifiers/spam/spam_classifer.pickle'))
topic_classifier = load(open('classifiers/topic/topic_classifier.pickle'))


class Classifier(object):

    def process(self, string):
        return dict(spam=self.get_spam_likelihood(string)[0],
                    ontopic=self.get_ontopic_likelihood(string)[0])

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
        return spam_classifier.predict_proba(txt.get_features())

    @staticmethod
    def get_ontopic_likelihood(string):
        return topic_classifier.predict([string])


if __name__ == "__main__":
    clf = Classifier()
    t = clf.process("""
                    Loan offer between particular
                    Need a quick loan for an emergency, for any procurement ... You are stuck to the bank or banking prohibited. We offer private loans online short and long term from 2000 $ to 1,500,000 $ RATE fixed 3% (depending on the type, amount and duration of the loan. Availability of funds within 3 days upon acceptance of your application . repayment period of 12 months to 98 months No hidden for more information please contact me by email clauses.. pret.particulier@outlook.com)
                    """)
    print(t)
