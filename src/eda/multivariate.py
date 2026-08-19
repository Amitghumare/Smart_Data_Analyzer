def get_numerical_column(df):
    return df.select_dtypes(include="number").columns.tolist()

def get_categorical_column(df):
    return df.select_dtypes(include=["object","category"]).columns.tolist()