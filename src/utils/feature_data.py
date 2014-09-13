"""
Series of functions to obtain features for the spam detector.
    params: data (str)
"""

from __future__ import division
from nltk.corpus import stopwords
import re
import pickle

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
        return max(len(re.findall(PHONEREGEX, self.str)), 0)

    def punct_ratio(self):
        return max(len(re.findall(PUNCREGEX, self.str)) / len(self.str), 0)

    def count_sensitive_words(self):
        return max(len(WATCHWORDS.intersection(set(self.str.split()))), 0)

    def get_features(self):
        return [self.count_urls(), self.count_phones(), self.punct_ratio(), self.count_sensitive_words()]
