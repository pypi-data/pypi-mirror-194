import pandas as pd
import sklearn
from sklearn.feature_selection import SelectKBest, mutual_info_regression
import numpy as np




def feature_selection_mutual_information(x_train, y_train, n):
    num = 10 ** n
    X_train_selected = pd.DataFrame()
    for i in range(n):
        k = 10 * (n - i)
        selector = SelectKBest(mutual_info_regression, k=k)
        selector.fit(x_train, y_train)
        X_train_selected = selector.transform(x_train)
    feature_list = X_train_selected.columns
    return X_train_selected



def fs_mutual_information(x_train, y_train, top = 10):
        Selector = SelectKBest(mutual_info_regression, top)
        Selector.fit(x_train,y_train)
        x_selected = Selector.transform(x_train)
        feature_list = x_selected.columns
        return feature_list


        
def feature_selection_correlation(x_train, y_train, bar = None, top = 10):
        y_name = y_train.columns[0]
        df = pd.concat([x_train, y_train], axis= 1)
        correlation = df.corr()
        correlation = correlation[correlation[y_train.columns] != 1]
        if bar == None:
            return None
        else:
               highly_corr = correlation.index[abs[correlation[y_name]] >= bar]
        x_selected = x_train[highly_corr]

               

        