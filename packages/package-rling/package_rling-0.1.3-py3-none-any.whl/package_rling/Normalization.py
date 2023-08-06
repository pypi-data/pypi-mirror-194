from sklearn.preprocessing import StandardScaler
from numpy import tanh
from sklearn.preprocessing import MinMaxScaler


def normalize_df(df):
    Scaler = StandardScaler()
    df_scaled = Scaler.fit_transform(df)
    return df_scaled

def tanh_df(df):
    return df.apply(tanh)

def maxmin_standardize_df(df)
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(df)
    return normalized_data


def 