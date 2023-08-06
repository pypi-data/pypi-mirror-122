import pandas as pd
from sklearn.model_selection import train_test_split # Import train_test_split function
from ml_models.evaluate import get_evaluation

def build_table(X, y,*args):
    '''
    X = predictor attributes
    y = acutal result

    *args = accepts model
    '''
    # Split dataset into training set and test set that donot require validation set
    df = pd.DataFrame()
    for model in args:
        if model[2]:
            X_train, X_remain, y_train, y_remain = train_test_split(X, y, test_size=0.4, random_state=1) # 60% training
            X_test, X_validation, y_test, y_validation = train_test_split(X_remain, y_remain, test_size=0.5) # 20% validation and 20% test
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1) # 80% training and 20% test
            
        classifier = model[0]
        name = model[1]
        classifier.fit(X_train,y_train)

        #Predict the response for test dataset
        y_pred = classifier.predict(X_test)
    
        score=classifier.predict_proba(X_test)[:, 1]
        df = df.append(get_evaluation(name, score, y_test, y_pred))
    return df