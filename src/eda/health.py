import pandas as pd


def calculate_data_health(df):

    if df is None or df.empty:
        return 0

    score = 100

    # Missing values
    total_cells = df.shape[0] * df.shape[1]

    if total_cells > 0:

        missing_percentage = (
            df.isnull().sum().sum()
            / total_cells
        ) * 100

        score -= missing_percentage * 0.5

    # Duplicate rows
    if len(df) > 0:

        duplicate_percentage = (
            df.duplicated().sum()
            / len(df)
        ) * 100

        score -= duplicate_percentage * 0.3

    # Clamp score
    score = max(
        0,
        min(100, score)
    )

    return round(score, 1)