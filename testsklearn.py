# -*- coding: utf-8 -*-

import numpy as np
from sklearn import datasets
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

iris = datasets.load_digits()
X, y = iris.data, iris.target
# X = np.random.randint(0, 2, size=[13053, 314])
# y = np.random.randint(0, 2, size=[13053, 1])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model1 = KNeighborsClassifier()
model2 = MultinomialNB()
model3 = LogisticRegression()
model4 = RandomForestClassifier()
model5 = SVC()

model1.fit(X_train, y_train)
predict1 = model1.predict(X_test)
accuracy1 = metrics.accuracy_score(y_test, predict1)

model2.fit(X_train, y_train)
predict2 = model2.predict(X_test)
accuracy2 = metrics.accuracy_score(y_test, predict2)

model3.fit(X_train, y_train)
predict3 = model3.predict(X_test)
accuracy3 = metrics.accuracy_score(y_test, predict3)

model4.fit(X_train, y_train)
predict4 = model4.predict(X_test)
accuracy4 = metrics.accuracy_score(y_test, predict4)

model5.fit(X_train, y_train)
predict5 = model5.predict(X_test)
accuracy5 = metrics.accuracy_score(y_test, predict5)


print(X.shape)
print(y.shape)
print(y_test.shape)
print(predict1.shape)
print(accuracy1)
print(accuracy2)
print(accuracy3)
print(accuracy4)
print(accuracy5)
