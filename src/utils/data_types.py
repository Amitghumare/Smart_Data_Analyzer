import pandas as pd
import numpy as np


# ============================================================
# BASIC COLUMN DETECTION
# ============================================================

def get_numeric_columns(df):

    if df is None or df.empty:
        return []

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def get_categorical_columns(df):

    if df is None or df.empty:
        return []

    return df.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    ).columns.tolist()


def get_datetime_columns(df):

    if df is None or df.empty:
        return []

    return df.select_dtypes(
        include=[
            "datetime64[ns]",
            "datetime64[ns, UTC]"
        ]
    ).columns.tolist()


# ============================================================
# AUTOMATIC DATE DETECTION
# ============================================================

def detect_date_columns(
    df,
    threshold=0.8
):

    if df is None or df.empty:
        return []

    date_columns = []

    for column in df.columns:

        # Already datetime
        if pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):

            date_columns.append(column)

            continue

        # Only try object/string columns
        if not (
            pd.api.types.is_object_dtype(
                df[column]
            )
            or
            pd.api.types.is_string_dtype(
                df[column]
            )
        ):

            continue

        try:

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_ratio = (
                converted.notna().mean()
            )

            if valid_ratio >= threshold:

                date_columns.append(column)

        except Exception:

            continue

    return date_columns


# ============================================================
# COLUMN INFORMATION
# ============================================================

def get_column_info(df):

    if df is None or df.empty:

        return pd.DataFrame(
            columns=[
                "column",
                "dtype",
                "non_null",
                "missing",
                "missing_percentage",
                "unique",
                "unique_percentage"
            ]
        )

    information = []

    total_rows = len(df)

    for column in df.columns:

        missing = int(
            df[column].isnull().sum()
        )

        unique = int(
            df[column].nunique(
                dropna=True
            )
        )

        if total_rows > 0:

            missing_percentage = (
                missing / total_rows
            ) * 100

            unique_percentage = (
                unique / total_rows
            ) * 100

        else:

            missing_percentage = 0

            unique_percentage = 0

        information.append({

            "column": column,

            "dtype": str(
                df[column].dtype
            ),

            "non_null": int(
                df[column].notnull().sum()
            ),

            "missing": missing,

            "missing_percentage":
                round(
                    missing_percentage,
                    2
                ),

            "unique": unique,

            "unique_percentage":
                round(
                    unique_percentage,
                    2
                )
        })

    return pd.DataFrame(
        information
    )


# ============================================================
# DATASET SUMMARY
# ============================================================

def get_dataset_summary(df):

    if df is None:

        return {

            "rows": 0,

            "columns": 0,

            "numeric_columns": [],

            "categorical_columns": [],

            "datetime_columns": [],

            "date_candidates": [],

            "missing_values": 0,

            "duplicate_rows": 0
        }

    numeric_columns = (
        get_numeric_columns(df)
    )

    categorical_columns = (
        get_categorical_columns(df)
    )

    datetime_columns = (
        get_datetime_columns(df)
    )

    date_candidates = (
        detect_date_columns(df)
    )

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "numeric_columns":
            numeric_columns,

        "categorical_columns":
            categorical_columns,

        "datetime_columns":
            datetime_columns,

        "date_candidates":
            date_candidates,

        "missing_values":
            int(
                df.isnull()
                .sum()
                .sum()
            ),

        "duplicate_rows":
            int(
                df.duplicated()
                .sum()
            )
    }


# ============================================================
# CONSTANT COLUMNS
# ============================================================

def get_constant_columns(df):

    if df is None or df.empty:

        return []

    constant_columns = []

    for column in df.columns:

        if df[column].nunique(
            dropna=False
        ) <= 1:

            constant_columns.append(
                column
            )

    return constant_columns


# ============================================================
# HIGH CARDINALITY COLUMNS
# ============================================================

def get_high_cardinality_columns(
    df,
    threshold=0.5
):

    if df is None or df.empty:

        return []

    result = []

    categorical = get_categorical_columns(
        df
    )

    for column in categorical:

        unique_ratio = (
            df[column].nunique(
                dropna=True
            )
            / len(df)
        )

        if unique_ratio >= threshold:

            result.append(column)

    return result


# ============================================================
# LOW CARDINALITY COLUMNS
# ============================================================

def get_low_cardinality_columns(
    df,
    max_unique=20
):

    if df is None or df.empty:

        return []

    result = []

    categorical = get_categorical_columns(
        df
    )

    for column in categorical:

        unique_count = df[column].nunique(
            dropna=True
        )

        if unique_count <= max_unique:

            result.append(column)

    return result