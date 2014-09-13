from sklearn import svm
from feature_data import FeatureData
import pandas as pd
import numpy as np
import pickle

training_data = pd.DataFrame.from_csv("spam_train.csv")

y = list(training_data.spam)
X = np.ndarray((len(training_data.spam), 4))
for i, data in enumerate(training_data.contents):
    X[i] = np.array(FeatureData(data).get_features())

testing_data = pd.DataFrame.from_csv("spam_test.csv")
y_test = list(testing_data.spam)
X_test = np.ndarray((len(testing_data.spam), 4))
for i, data in enumerate(testing_data.contents):
    X_test[i] = np.array(FeatureData(data).get_features())

clf = svm.SVC(class_weight='auto')
clf.fit(X, y)
print clf.score(X_test, y_test)

with open("spam_classifer.pickle", "w+") as spam_classifer:
    spam_classifer.write(pickle.dumps(clf))
