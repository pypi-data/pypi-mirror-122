pypi url :: [https://pypi.org/project/ml-models/]
This repository is stacked with the multiple ml models looped over certain times, 

The User can install the ml_models and use the project as shown in driver package. 

The data needs to be concise and at last you'll have a table generated over different ml models with different evaluation technique. With this you can directly check the model to use for.
```
from ml_models import *
from ml_models.build_model import build_table

random_forest_classifier= RandomForestClassifier(n_estimators= 10, criterion="entropy")  

# for decision Tree
# Create Decision Tree classifer object
decision_tree = DecisionTreeClassifier()


nn = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(1), random_state=1)



if __name__ == '__main__':
       # reading the csv file
    df = pd.read_csv("data.csv")
    X = df.iloc[:, :-1] # Features
    y = df.iloc[:, -1] # Target variable

    li_df = []
    for i in range(0,10):
        li_df.append(build_table(X,y,[decision_tree,"Decision Tree",False],
                                [nn, "Artificial Neural Network",True]))

    averages = pd.concat([each.stack() for each in li_df],axis=1)\
                .apply(lambda x:x.mean(),axis=1)\
                .unstack()
    print(averages)


```