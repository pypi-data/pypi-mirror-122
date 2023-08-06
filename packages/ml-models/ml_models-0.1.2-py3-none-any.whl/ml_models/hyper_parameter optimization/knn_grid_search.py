# Using Grid Search for hyper parameter optimization

from sklearn.model_selection import GridSearchCV
from ml_models import KNeighborsClassifier

grid_params = {
    'n_neighbors':[1,3, 5],
    'weights':['uniform','distance'],
    'metric':['euclidean', 'manhattan','minkowski'],
    'p':[2]
    }

def grid_search(X_train, y_train, grid_params=grid_params) -> int:
    '''
    grid params accepts different hyper parameters
    '''
    gs = GridSearchCV(KNeighborsClassifier(),
                  grid_params,
                  verbose=1,
                  n_jobs=-1 # no.of processor total use 
    )
    gs_results = gs.fit(X_train,y_train)
    return gs_results.best_params_["n_neighbors"]