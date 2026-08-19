import pandas as pd


def remove_duplicates(df):
    return df.drop_duplicates().copy()


def drop_missing_rows(df):
    return df.dropna().copy()


def fill_missing_mean(df, column):

    result = df.copy()

    result[column] = pd.to_numeric(
        result[column],
        errors="coerce"
    )

    result[column] = result[column].fillna(
        result[column].mean()
    )

    return result


def fill_missing_median(df, column):

    result = df.copy()

    result[column] = pd.to_numeric(
        result[column],
        errors="coerce"
    )

    result[column] = result[column].fillna(
        result[column].median()
    )

    return result


def fill_missing_mode(df, column):

    result = df.copy()

    mode = result[column].mode()

    if not mode.empty:
        result[column] = result[column].fillna(
            mode.iloc[0]
        )

    return result


def fill_missing_custom(df, column, value):

    result = df.copy()

    result[column] = result[column].fillna(value)

    return result


def convert_to_numeric(df, column):

    result = df.copy()

    result[column] = pd.to_numeric(
        result[column],
        errors="coerce"
    )

    return result


def convert_to_string(df, column):

    result = df.copy()

    result[column] = (
        result[column]
        .astype(str)
    )

    return result


def convert_to_datetime(df, column):

    result = df.copy()

    result[column] = pd.to_datetime(
        result[column],
        errors="coerce"
    )

    return result


def remove_outliers_iqr(df, column):

    result = df.copy()

    data = pd.to_numeric(
        result[column],
        errors="coerce"
    )

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    mask = (
        (data >= lower_bound)
        &
        (data <= upper_bound)
    )

    

    return result[
        mask | data.isna()
    ].copy()

def get_cleaning_summary(
    original_df,
    cleaned_df
):

    summary = {}

    summary["original_rows"] = (
        original_df.shape[0]
    )

    summary["cleaned_rows"] = (
        cleaned_df.shape[0]
    )

    summary["original_columns"] = (
        original_df.shape[1]
    )

    summary["cleaned_columns"] = (
        cleaned_df.shape[1]
    )

    summary["original_missing"] = int(
        original_df.isnull().sum().sum()
    )

    summary["remaining_missing"] = int(
        cleaned_df.isnull().sum().sum()
    )

    summary["duplicates_removed"] = (
        int(original_df.duplicated().sum())
        -
        int(cleaned_df.duplicated().sum())
    )

    return summary