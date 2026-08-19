import pandas as pd


def numerical_insights(df):

    insights = []

    numeric_columns = (
        df
        .select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )

    for column in numeric_columns:

        data = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if data.empty:
            continue

        mean = data.mean()
        median = data.median()
        minimum = data.min()
        maximum = data.max()
        outlier_count = detect_outliers(
            df,
            column
)

        if outlier_count > 0:

         insights.append(
         f"🚨 **{column}** has approximately "
         f"**{outlier_count} potential outliers** "
         f"using the IQR method."
    )

        # ------------------------------------------
        # Mean vs Median
        # ------------------------------------------

        if mean > median * 1.1:

            insights.append(
                f"📈 **{column}** appears to be "
                f"right-skewed because its mean "
                f"({mean:.2f}) is higher than its "
                f"median ({median:.2f})."
            )

        elif median > mean * 1.1:

            insights.append(
                f"📉 **{column}** appears to be "
                f"left-skewed because its median "
                f"({median:.2f}) is higher than its "
                f"mean ({mean:.2f})."
            )

        # ------------------------------------------
        # Range
        # ------------------------------------------

        if mean != 0:

            range_ratio = (
                (maximum - minimum)
                / abs(mean)
            )

            if range_ratio > 5:

                insights.append(
                    f"📊 **{column}** has a wide "
                    f"range from {minimum:.2f} "
                    f"to {maximum:.2f}."
                )

        # ------------------------------------------
        # Highest Value
        # ------------------------------------------

        insights.append(
            f"🔝 **{column}** has a maximum "
            f"value of {maximum:.2f} and a "
            f"minimum value of {minimum:.2f}."
        )

    

    return insights

def detect_outliers(df, column):

    data = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if data.empty:
        return 0

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = (
        (data < lower)
        |
        (data > upper)
    )

    return int(outliers.sum())