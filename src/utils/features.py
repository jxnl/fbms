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


def countURL(data):
    d = re.findall(URLREGEX, data)
    return len(d)


def countPhones(data):
    return max(len(re.findall(PHONEREGEX, data)), 0)


def punctuationRatio(data):
    return max(len(re.findall(PUNCREGEX, data)) / len(data), 0)


def numberOfSensitiveWords(data):
    return max(len(WATCHWORDS.intersection(set(data.split()))), 0)


def capitalizedWordCount(data):
    return max(len([w for w in data.split() if w.isupper()]), 0)
