def remove_whitespace(df, column):

    df = df.copy()

    df[column] = df[column].astype(str).str.strip()

    return df


def convert_to_lowercase(df, column):

    df = df.copy()

    df[column] = (
        df[column]
        .astype(str)
        .str.lower()
    )

    return df


def convert_to_uppercase(df, column):


    df = df.copy()

    df[column] = (
        df[column]
        .astype(str)
        .str.upper()
    )

    return df