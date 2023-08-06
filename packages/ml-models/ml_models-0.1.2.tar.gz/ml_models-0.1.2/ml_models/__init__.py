__version__ = '0.1.0'

from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

#load libraries
import pandas as pd 
import numpy as np
from matplotlib import pyplot  as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# importing required libaries
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.ensemble import RandomForestClassifier  
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.naive_bayes import GaussianNB  
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
