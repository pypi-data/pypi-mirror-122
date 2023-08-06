from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import pandas as pd

def get_evaluation(method, score, y_test, y_pred):

    '''
    Accuracy, MCC,F1 Score, TP, TN, pr_auc, roc_auc_curve 
    '''
    accuracy = metrics.accuracy_score(y_test, y_pred)
#     print("Accuracy:",accuracy)

    mathew = metrics.matthews_corrcoef(y_test, y_pred)
#     print("MCC:", mathew)

    f1_score = metrics.f1_score(y_test,y_pred)
#     print("F1 score: ", f1_score)

    TP = metrics.recall_score(y_test, y_pred)
#     print("TP:",TP)

    TN = metrics.precision_score(y_test, y_pred)
#     print("TN", TN)

    pr_auc =metrics.average_precision_score(y_test,y_pred)
#     print("Precision Recall auc", pr_auc)
    
    roc_auc_score = metrics.roc_auc_score(y_test,score )
#     print("roc_auc_score", roc_auc_score)
    df = pd.DataFrame(data=[[round(accuracy,3), round(mathew,3), round(f1_score,3), round(TP,3), round(TN,3), round(pr_auc,3), round(roc_auc_score,3)]], columns=['MCC', 'F1 Score', 'Accuracy', 'TP Rate', 'TN Rate', 'PR AUC', 'ROC AUC'])
    df.index=[method]
    return df