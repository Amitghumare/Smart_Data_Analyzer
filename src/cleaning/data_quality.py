import pandas as pd
import numpy as np


def generate_data_quality_report(df):

    report = {}

    # ==================================================
    # BASIC INFORMATION
    # ==================================================

    report["rows"] = df.shape[0]

    report["columns"] = df.shape[1]

    report["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    report["total_missing"] = int(
        df.isnull().sum().sum()
    )


    # ==================================================
    # MISSING VALUES
    # ==================================================

    missing = (
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
    )

    report["missing_columns"] = (
        missing[
            missing > 0
        ].to_dict()
    )


    # ==================================================
    # DATA TYPES
    # ==================================================

    report["data_types"] = (
        df.dtypes
        .astype(str)
        .to_dict()
    )


    # ==================================================
    # CONSTANT COLUMNS
    # ==================================================

    constant_columns = []

    for column in df.columns:

        if df[column].nunique(
            dropna=False
        ) <= 1:

            constant_columns.append(
                column
            )

    report["constant_columns"] = (
        constant_columns
    )


    # ==================================================
    # HIGH CARDINALITY
    # ==================================================

    high_cardinality = []

    for column in df.select_dtypes(
        include=["object", "category"]
    ).columns:

        unique_count = (
            df[column]
            .nunique(
                dropna=True
            )
        )

        if (
            unique_count
            > 0.5 * len(df)
        ):

            high_cardinality.append(
                column
            )

    report["high_cardinality_columns"] = (
        high_cardinality
    )


    # ==================================================
    # NUMERICAL COLUMNS
    # ==================================================

    numerical_columns = (
        df.select_dtypes(
            include=np.number
        ).columns.tolist()
    )

    report["numerical_columns"] = (
        numerical_columns
    )


    # ==================================================
    # CATEGORICAL COLUMNS
    # ==================================================

    categorical_columns = (
        df.select_dtypes(
            include=[
                "object",
                "category"
            ]
        ).columns.tolist()
    )

    report["categorical_columns"] = (
        categorical_columns
    )


    # ==================================================
    # POTENTIAL OUTLIERS
    # ==================================================

    outliers = {}

    for column in numerical_columns:

        series = df[column].dropna()

        if len(series) < 5:

            continue

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:

            continue

        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )

        count = (
            (
                (series < lower_bound)
                |
                (series > upper_bound)
            )
            .sum()
        )

        if count > 0:

            outliers[column] = int(
                count
            )

    report["outliers"] = outliers


    # ==================================================
    # NEGATIVE VALUES
    # ==================================================

    negative_values = {}

    for column in numerical_columns:

        count = (
            df[column] < 0
        ).sum()

        if count > 0:

            negative_values[column] = int(
                count
            )

    report["negative_values"] = (
        negative_values
    )


    # ==================================================
    # POSSIBLE DATE COLUMNS
    # ==================================================

    possible_dates = []

    for column in df.columns:

        if df[column].dtype == "object":

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_ratio = (
                converted.notna().mean()
            )

            if valid_ratio >= 0.7:

                possible_dates.append(
                    column
                )

    report["possible_date_columns"] = (
        possible_dates
    )


    return report