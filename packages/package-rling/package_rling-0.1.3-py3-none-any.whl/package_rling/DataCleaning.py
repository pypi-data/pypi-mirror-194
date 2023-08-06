import pandas as pd

def drop_nan(df = pd.DataFrame(), col = None, row = None, axis = 1):
    if axis == 0:
        if row = None:
            raise Exception('No percentage of value input, try "row  = XXX" then run again')
        elif col == None:
            df = df.dropna(thresh=int(df.shape[1]*row), axis = 0)
        else:
            df = df.dropna(thresh=int(df.shape[1]*row), axis = 0)
            df = df.dropna(thresh=int(df.shape[0]*col), axis = 1)
    if axis ==1:
        if col = None:
            raise Exception('No percentage of value input, try "col  = XXX" then run again')
        elif row == None:
            df = df.dropna(thresh=int(df.shape[0]*row), axis = 1)
        else:
            df = df.dropna(thresh=int(df.shape[0]*row), axis = 1)
            df = df.dropna(thresh=int(df.shape[1]*col), axis = 0)
    
    return df

