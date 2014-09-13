"""
Series of functions to obtain features for the spam detector.
    params: data (str)
"""

from __future__ import division
from nltk.corpus import stopwords
import pickle
import re

URLREGEX = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
PHONEREGEX = "(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?"
PUNCREGEX = "[*=-_$%#@~`]"
WATCHWORDS = pickle.loads(open("watchwords.pickle").read())

class FeatureData:
    def __init__(self, str):
        self.str = str

    def count_urls(self):
        d = re.findall(URLREGEX, self.str)
        return len(d)

    def count_phones(self):
        return self.__max_of_iter(re.findall(PHONEREGEX, self.str))

    def count_sensitive_words(self):
        return self.__max_of_iter(WATCHWORDS.intersection(set(self.str.split())))

    def capitalize_word_count(self):
        return self.__max_of_iter(filter(lambda x: x.isupper(), self.str))

    def __max_of_iter(self, iterable):
        return max(len(iterable), 0)

    def get_features(self):
        return [self.count_urls(),
                self.count_phones(),
                self.capitalize_word_count(),
                self.count_sensitive_words()]
