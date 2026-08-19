import pandas as pd
import numpy as np


# ============================================================
# DATASET OVERVIEW
# ============================================================

def get_dataset_overview(df):

    overview = {

        "rows": df.shape[0],

        "columns": df.shape[1],

        "total_cells":
            df.shape[0] * df.shape[1],

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
            ),

        "numerical_columns":
            len(
                df.select_dtypes(
                    include=np.number
                ).columns
            ),

        "categorical_columns":
            len(
                df.select_dtypes(
                    include=[
                        "object",
                        "category"
                    ]
                ).columns
            )
    }

    return overview


# ============================================================
# NUMERICAL SUMMARY
# ============================================================

def get_numerical_summary(df):

    numerical_df = (
        df.select_dtypes(
            include=np.number
        )
    )

    if numerical_df.empty:

        return pd.DataFrame()

    summary = (
        numerical_df
        .describe()
        .T
        .reset_index()
    )

    summary = summary.rename(
        columns={
            "index": "Column"
        }
    )

    return summary


# ============================================================
# CATEGORICAL SUMMARY
# ============================================================

def get_categorical_summary(df):

    categorical_columns = (
        df.select_dtypes(
            include=[
                "object",
                "category"
            ]
        )
        .columns
    )

    if len(categorical_columns) == 0:

        return pd.DataFrame()

    rows = []

    for column in categorical_columns:

        series = df[column]

        rows.append({

            "Column":
                column,

            "Unique Values":
                series.nunique(
                    dropna=True
                ),

            "Missing Values":
                int(
                    series.isnull()
                    .sum()
                ),

            "Most Frequent":
                (
                    series
                    .mode()
                    .iloc[0]
                    if not series.mode().empty
                    else "N/A"
                ),

            "Frequency":
                (
                    int(
                        series
                        .value_counts(
                            dropna=True
                        )
                        .iloc[0]
                    )
                    if not series
                    .value_counts(
                        dropna=True
                    )
                    .empty
                    else 0
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# MISSING VALUE SUMMARY
# ============================================================

def get_missing_summary(df):

    missing = (
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
    )

    missing = missing[
        missing > 0
    ]

    if missing.empty:

        return pd.DataFrame()

    result = pd.DataFrame({

        "Column":
            missing.index,

        "Missing Values":
            missing.values,

        "Percentage":
            (
                missing.values
                / len(df)
                * 100
            ).round(2)
    })

    return result


# ============================================================
# UNIQUE VALUE SUMMARY
# ============================================================

def get_unique_summary(df):

    rows = []

    for column in df.columns:

        rows.append({

            "Column":
                column,

            "Unique Values":
                df[column]
                .nunique(
                    dropna=True
                ),

            "Data Type":
                str(
                    df[column].dtype
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# CORRELATION MATRIX
# ============================================================

def get_correlation_matrix(df):

    numerical_df = (
        df.select_dtypes(
            include=np.number
        )
    )

    if numerical_df.shape[1] < 2:

        return pd.DataFrame()

    return numerical_df.corr(
        numeric_only=True
    )


# ============================================================
# OUTLIER SUMMARY
# ============================================================

def get_outlier_summary(df):

    numerical_columns = (
        df.select_dtypes(
            include=np.number
        ).columns
    )

    rows = []

    for column in numerical_columns:

        series = df[column].dropna()

        if len(series) < 5:

            continue

        q1 = series.quantile(
            0.25
        )

        q3 = series.quantile(
            0.75
        )

        iqr = q3 - q1

        if iqr == 0:

            continue

        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )

        outlier_count = int(
            (
                (series < lower_bound)
                |
                (series > upper_bound)
            ).sum()
        )

        rows.append({

            "Column":
                column,

            "Q1":
                round(q1, 2),

            "Q3":
                round(q3, 2),

            "Lower Bound":
                round(
                    lower_bound,
                    2
                ),

            "Upper Bound":
                round(
                    upper_bound,
                    2
                ),

            "Outliers":
                outlier_count
        })

    return pd.DataFrame(rows)


# ============================================================
# FULL EDA REPORT
# ============================================================

def generate_eda_report(df):

    report = {

        "overview":
            get_dataset_overview(df),

        "numerical_summary":
            get_numerical_summary(df),

        "categorical_summary":
            get_categorical_summary(df),

        "missing_summary":
            get_missing_summary(df),

        "unique_summary":
            get_unique_summary(df),

        "correlation":
            get_correlation_matrix(df),

        "outliers":
            get_outlier_summary(df)
    }

    return report