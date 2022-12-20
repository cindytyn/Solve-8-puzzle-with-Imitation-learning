# -*- coding: utf-8 -*-
"""cmpt417_model_xgboost.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17dMd1ucjubHwstLAPmpGRLApW4NSC71k
"""

import numpy as np
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("/content/drive/MyDrive/uni/CMPT417/cmpt417finalproject/s3_train3_csv.csv")
df = df.iloc[:,1:]
df.head()

df_test = pd.read_csv("/content/drive/MyDrive/uni/CMPT417/cmpt417finalproject/s3_test2_csv.csv")
df_test = df_test.iloc[:,1:]
df_test.head()

pList = []
cList = []
pList.append(df['previous_state'])
cList.append(df['current_state'])

pList_test = []
cList_test = []
pList_test.append(df_test['previous_state'])
cList_test.append(df_test['current_state'])

def flatten_list(configList):
  flatten_list = []
  for x in configList:
    for y in x: #this gets [[0, 1, 3], [7, 8, 2], [5, 4, 6]] [[0, 1, 3], [7, 8, 2], [5, 4, 6]]
      nested_list = []
      for s in y: #this gets every element as a string
        if s.isdigit():
          nested_list.append(int(s))
      flatten_list.append(nested_list)
  print(flatten_list)
  return flatten_list

X = flatten_list(pList)
Y = flatten_list(cList)

X_test = flatten_list(pList_test)
Y_test = flatten_list(cList_test)

x = pd.DataFrame(X)
x_test = pd.DataFrame(X_test)

y = np.array(Y)
y_test = np.array(Y_test)

from xgboost import XGBClassifier
from sklearn.multioutput import MultiOutputClassifier

params = {  
            'min_child_weight': [1, 5],
            'max_depth': [3,6,10],
            'n_estimators': [20,50,100,200]
        }

xgboost_model = XGBClassifier(n_estimators=500, max_depth=10, min_child_weight=1, learning_rate=0.1, booster='gbtree', objective='binary:logistic')
classifier = MultiOutputClassifier(xgboost_model, n_jobs=-1)
# fit model
classifier.fit(x, y)

x# make predictions
preds = classifier.predict(x_test)

classifier.score(x_test,y_test)