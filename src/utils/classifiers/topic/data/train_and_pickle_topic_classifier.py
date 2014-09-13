from __future__ import print_function
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from csv import reader
import pickle

# LOADING IN DATA
X, y = [], []
with open("train_topic.csv") as train:
    dreader = reader(train, delimiter=',')
    for row in dreader:
        _, target, data = row
        X.append(data)
        y.append(target)
t_data = dict(data=X, target=y)

X_test, y_test = [], []
with open("test_topic.csv") as test:
    dreader = reader(test, delimiter=',')
    for row in dreader:
        _, target, data = row
        X_test.append(data)
        y_test.append(target)
test_data = dict(data=X_test, target=y_test)

SGD = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier())])

SGD.set_params(vect__max_df=0.5,
               vect__max_features=None,
               vect__ngram_range=(1, 2),
               clf__alpha=1e-05,
               clf__penalty='l2',
               tfidf__use_idf=True).fit(t_data['data'], t_data['target'])

with open("topic_classifier.pickle", 'w+') as tc:
    pickle.dump(SGD, tc)
