import pandas as pd
from sklearn import svm
import numpy as np
import features as ft

training_data = pd.DataFrame.from_csv("spam_train.csv")
y = list(training_data.spam)
X = np.ndarray((len(training_data.spam), 4))
for i, data in enumerate(training_data.contents):
    X[i] = np.array(obtainFeatures(data))

testing_data = pd.DataFrame.from_csv("spam_test.csv")
y_test = list(testing_data.spam)
X_test = np.ndarray((len(testing_data.spam), 4))
for i, data in enumerate(testing_data.contents):
    X_test[i] = np.array(obtainFeatures(data))

clf = svm.SVC(class_weight='auto')
clf.fit(X, y)


