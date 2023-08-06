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


def feature_selection_correlation(x_train, y_train, n):
    corr_matrix = pd.concat([x_train, y_train], axis=1).corr()
    top_n_features = np.abs(corr_matrix.iloc[:-1, -1]).nlargest(n).index.tolist()
    X_train_selected = x_train[top_n_features]
    return X_train_selected


def feature_selection_correlation2(x_train, y_train):
    df = pd.concat([x_train, y_train], axis=1)
    correlations = df.corr()
    correlations = correlations[correlations['I00353US Index'] != 1]
    highly_correlated_features = correlations.index[abs(correlations['I00353US Index']) > 0.1]
    X_train_selected = x_train[highly_correlated_features]
    return X_train_selected  

