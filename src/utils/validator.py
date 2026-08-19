import pandas as pd
import numpy as np


def validate_dataset(df):
    """
    Validate a pandas DataFrame.

    Returns:
        valid: bool
        errors: list
        warnings: list
    """

    errors = []
    warnings = []

    # ========================================================
    # DATAFRAME CHECK
    # ========================================================

    if df is None:

        errors.append(
            "Dataset is empty or could not be loaded."
        )

        return False, errors, warnings


    if not isinstance(df, pd.DataFrame):

        errors.append(
            "Uploaded data is not a valid pandas DataFrame."
        )

        return False, errors, warnings


    # ========================================================
    # EMPTY DATASET
    # ========================================================

    if df.empty:

        errors.append(
            "The uploaded dataset contains no rows."
        )

        return False, errors, warnings


    # ========================================================
    # NO COLUMNS
    # ========================================================

    if len(df.columns) == 0:

        errors.append(
            "The dataset does not contain any columns."
        )

        return False, errors, warnings


    # ========================================================
    # DUPLICATE COLUMN NAMES
    # ========================================================

    duplicate_columns = (
        df.columns[
            df.columns.duplicated()
        ]
        .tolist()
    )

    if duplicate_columns:

        warnings.append(
            "Duplicate column names detected: "
            +
            ", ".join(
                map(
                    str,
                    duplicate_columns
                )
            )
        )


    # ========================================================
    # EMPTY COLUMN NAMES
    # ========================================================

    empty_columns = [

        column

        for column in df.columns

        if (
            column is None
            or
            str(column).strip() == ""
        )

    ]

    if empty_columns:

        warnings.append(
            "One or more columns have empty names."
        )


    # ========================================================
    # ALL MISSING COLUMNS
    # ========================================================

    all_missing_columns = [

        column

        for column in df.columns

        if df[column].isna().all()

    ]

    if all_missing_columns:

        warnings.append(
            "Columns containing only missing values: "
            +
            ", ".join(
                map(
                    str,
                    all_missing_columns
                )
            )
        )


    # ========================================================
    # HIGH MISSING VALUES
    # ========================================================

    missing_percentage = (
        df.isnull()
        .mean()
        * 100
    )

    high_missing_columns = (
        missing_percentage[
            missing_percentage > 50
        ]
        .index
        .tolist()
    )

    if high_missing_columns:

        warnings.append(
            "More than 50% of values are missing in: "
            +
            ", ".join(
                map(
                    str,
                    high_missing_columns
                )
            )
        )


    # ========================================================
    # DUPLICATE ROWS
    # ========================================================

    duplicate_rows = int(
        df.duplicated()
        .sum()
    )

    if duplicate_rows > 0:

        warnings.append(
            f"{duplicate_rows:,} duplicate rows detected."
        )


    # ========================================================
    # CONSTANT COLUMNS
    # ========================================================

    constant_columns = []

    for column in df.columns:

        if (
            df[column]
            .nunique(
                dropna=True
            )
            <= 1
        ):

            constant_columns.append(
                column
            )

    if constant_columns:

        warnings.append(
            "Constant columns detected: "
            +
            ", ".join(
                map(
                    str,
                    constant_columns
                )
            )
        )


    # ========================================================
    # NUMERICAL COLUMNS
    # ========================================================

    numeric_columns = (
        df.select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )

    if not numeric_columns:

        warnings.append(
            "No numerical columns were detected. "
            "Statistical and correlation analysis "
            "will be limited."
        )


    # ========================================================
    # CATEGORICAL COLUMNS
    # ========================================================

    categorical_columns = (
        df.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        )
        .columns
        .tolist()
    )

    if not categorical_columns:

        warnings.append(
            "No categorical columns were detected."
        )


    return True, errors, warnings