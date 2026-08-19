def get_duplicate_count(df):
    return int(df.duplicated().sum())

def remove_duplicates(df):
    df = df.copy()

    df = df.drop_duplicates()

    return df