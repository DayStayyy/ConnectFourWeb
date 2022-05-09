import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('../input/connect-4/c4_game_database.csv')
df.shape
df.head()
df.tail()
df.isnull().sum()   
df= df.dropna()

fig = plt.figure(figsize = (22,18))
ax = fig.gca()
df.hist(ax=ax)
plt.show()

X = df.drop('winner', axis = 1)
y = df['winner']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35,random_state=42)
model_1 = RandomForestClassifier(max_depth=30, random_state=15)
model_1.fit(X_train, y_train)
y_pred = model_1.predict(X_test)
accuracy_score(y_test,y_pred)