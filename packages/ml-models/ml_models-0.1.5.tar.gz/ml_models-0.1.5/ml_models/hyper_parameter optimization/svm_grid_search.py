
# FOR SVM linear 
from sklearn.model_selection import GridSearchCV
from ml_models import SVC
 
# defining parameter range
param_grid = {'C': [0.1, 1, 10],
              'gamma': [1, 0.1, 0.01],
              'kernel': ['linear']}

def grid_search(X_train, y_train, param_grid=param_grid):
    '''
    grid params accepts different hyper parameters
    '''
    grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 1)
 
    # fitting the model for grid search
    grid.fit(X_train, y_train)

    # print best parameter after tuning
    print(grid.best_params_)
    
    # print how our model looks after hyper-parameter tuning
    print(grid.best_estimator_)
    return grid