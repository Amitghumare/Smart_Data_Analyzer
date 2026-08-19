import pandas as pd

def get_dataset_shape(df):
    rows,columns = df.shape

    return rows,columns

def get_missing_values(df):
    return int(df.isnull().sum().sum())

def get_duplicated_row(df):
    return int(df.duplicated().sum())

def get_numerical_columns(df):
    return df.select_dtypes(
        include=["int64","float64"]
    ).columns.tolist()

def get_categorical_columns(df):
    return df.select_dtypes(include=["object","category"]).columns.tolist()

def get_data_type(df):
    return df.dtypes

def get_missing_by_columns(df):
    return df.isnull().sum()