from src.insights.numerical import (
    numerical_insights
)

from src.insights.categorical import (
    categorical_insights
)

from src.insights.correlation import (
    correlation_insights
)


def generate_insights(df):

    insights = []

    # ----------------------------------------------
    # Dataset information
    # ----------------------------------------------

    rows = df.shape[0]
    columns = df.shape[1]

    insights.append(
        f"📊 The dataset contains "
        f"**{rows:,} rows** and "
        f"**{columns} columns**."
    )

    # ----------------------------------------------
    # Missing values
    # ----------------------------------------------

    total_missing = int(
        df.isnull()
        .sum()
        .sum()
    )

    total_cells = (
        df.shape[0]
        * df.shape[1]
    )

    if total_cells > 0:

        missing_percentage = (
            total_missing
            / total_cells
            * 100
        )

    else:

        missing_percentage = 0


    if total_missing == 0:

        insights.append(
            "✅ The dataset contains "
            "no missing values."
        )

    else:

        insights.append(
            f"⚠️ The dataset contains "
            f"**{total_missing:,} missing values** "
            f"({missing_percentage:.2f}% of all cells)."
        )

    # ----------------------------------------------
    # Duplicate rows
    # ----------------------------------------------

    duplicates = int(
        df.duplicated()
        .sum()
    )

    if duplicates == 0:

        insights.append(
            "✅ No duplicate rows were detected."
        )

    else:

        insights.append(
            f"🔁 The dataset contains "
            f"**{duplicates:,} duplicate rows**."
        )

    # ----------------------------------------------
    # Numerical insights
    # ----------------------------------------------

    insights.extend(
        numerical_insights(df)
    )

    # ----------------------------------------------
    # Categorical insights
    # ----------------------------------------------

    insights.extend(
        categorical_insights(df)
    )

    # ----------------------------------------------
    # Correlation insights
    # ----------------------------------------------

    insights.extend(
        correlation_insights(df)
    )

    return insights