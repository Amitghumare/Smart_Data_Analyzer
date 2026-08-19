def get_numeric_statistics(df):
    return df.describe().T

def get_categorical_statistics(df):
    return df.describe(include="object").T