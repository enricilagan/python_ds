"""
Variable	Definition	Key
survival	Survival	0 = No, 1 = Yes
pclass		Ticket class	1 = 1st = Upper, 2 = 2nd = Middle, 3 = 3rd = Lower
sex			Sex	
Age			Age in years (fractional if less than 1. If the age is estimated, is it in the form of xx.5)
sibsp		# of siblings / spouses aboard the Titanic	
	Sibling = brother, sister, stepbrother, stepsister
	Spouse = husband, wife (mistresses and fiancés were ignored)
parch		# of parents / children aboard the Titanic	
	Parent = mother, father
	Child = daughter, son, stepdaughter, stepson
	Some children travelled only with a nanny, therefore parch=0 for them.
ticket		Ticket number	
fare		Passenger fare	
cabin		Cabin number	
embarked	Port of Embarkation	C = Cherbourg, Q = Queenstown, S = Southampton
"""

# import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import re
import os

# make python folder your current working directory
if os.path.isdir('python'):
	os.chdir('python')

# Load titanic data frame
titanic_train = pd.read_csv('train.csv')
titanic_test = pd.read_csv('test.csv')

df = [titanic_train, titanic_test]
titanic = pd.concat(df)

# Data exploration
titanic.head()
titanic.info()
titanic.describe()

def change_col(data):
 new_col = [i.lower().replace(' ','_').replace('#','no') for i in data.columns]
 data.columns = new_col
 return data

 titanic = change_col(titanic)
 
titanic['name_split'] = titanic.name.str.split(',')
titanic['lastname'] = titanic.name_split.str.get(0)
titanic['firstname'] = titanic.name_split.str.get(1)


