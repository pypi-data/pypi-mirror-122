from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV


# Create list of hyperparameters 
max_iter = [10, 20]
hidden_layer_sizes = [(1, )]
param_grid = {'max_iter': max_iter, 'hidden_layer_sizes': hidden_layer_sizes}

def grid_search(X_train, y_train, param_grid=param_grid):
    '''
    grid params accepts different hyper parameters
    '''
    # Use Grid search CV to find best parameters using 4 jobs
    mlp = MLPClassifier()
    clf = GridSearchCV(estimator = mlp, param_grid = param_grid, 
                    scoring = 'roc_auc', n_jobs = 4)
    clf.fit(X_train, y_train)
    print("Best Score: ")
    print(clf.best_score_)
    print("Best Estimator: ")
    print(clf.best_estimator_)
    return clf