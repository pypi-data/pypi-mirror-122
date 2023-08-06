from ml_models import *
from ml_models.build_model import build_table

random_forest_classifier= RandomForestClassifier(n_estimators= 10, criterion="entropy")  

# for decision Tree
# Create Decision Tree classifer object
decision_tree = DecisionTreeClassifier()


# Gradient Boosting Classifier
gradient = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0)


# Logistic Regression
reg = LogisticRegression()
# regression 
##Y=e(Xb)1+e(Xb)

# KNCLAssifier
# from grid search above estimated
knn= KNeighborsClassifier(n_neighbors=3, metric='minkowski', p=2)  

#NAIVE BAYES MODEL

#1. gaussian, 2.Bernoulli 3.Multinomial

naive_bayes = GaussianNB()  

#Hyper parameter
# SVM classifier 

radial = SVC(kernel = 'rbf', C = 10, gamma = 0.1, probability=True)

linear = SVC(kernel = 'linear', C = 0.1, gamma = 0.1, probability=True)


# Multi layer perceptron Neural network

nn = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(1), random_state=1)


if __name__ == '__main__':
    # reading the csv file
    df = pd.read_csv("heart_failure_records.csv")
    X = df.iloc[:, :-1] # Features
    y = df.iloc[:, -1] # Target variable

    li_df = []
    for i in range(0,10):
        li_df.append(build_table(X,y,[random_forest_classifier,"Random Forest",False],[decision_tree,"Decision Tree",False],
                                [gradient,"Gradient Boosting",False],[reg,"Linear Regression",False],
                                [naive_bayes, "Naive Bayes",False],
                                [knn, "K Neighbors classifier",True],
                                [radial,"SVM Radial",True],[radial,"SVM Linear",True],
                                [nn, "Artificial Neural Network",True]))

    averages = pd.concat([each.stack() for each in li_df],axis=1)\
                .apply(lambda x:x.mean(),axis=1)\
                .unstack()
    print(averages)
        