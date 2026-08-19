import pandas as pd

def convert_to_numeric(df, column):
    df = df.copy()

    df[column]=pd.to_numeric(df[column],errors = "coerce")

    return df

def convert_to_datetime(df, column):
    df= df.copy()
    df[column]=pd.to_datetime(df[column],errors="coerce")

    return df