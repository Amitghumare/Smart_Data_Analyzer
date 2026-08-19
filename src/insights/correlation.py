def correlation_insights(df):

    insights = []

    numeric_df = (
        df
        .select_dtypes(
            include="number"
        )
    )

    if numeric_df.shape[1] < 2:

        return insights

    correlation = numeric_df.corr()

    columns = correlation.columns

    relationships = []

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            value = correlation.iloc[
                i,
                j
            ]

            if value != value:
                continue

            relationships.append(
                (
                    columns[i],
                    columns[j],
                    value
                )
            )

    relationships.sort(
        key=lambda x: abs(x[2]),
        reverse=True
    )

    # ----------------------------------------------
    # Strong relationships
    # ----------------------------------------------

    for column1, column2, value in relationships:

        if abs(value) >= 0.7:

            direction = (
                "positive"
                if value > 0
                else "negative"
            )

            insights.append(
                f"🔗 **{column1}** and "
                f"**{column2}** have a strong "
                f"{direction} correlation "
                f"({value:.2f})."
            )

        elif abs(value) >= 0.5:

            direction = (
                "positive"
                if value > 0
                else "negative"
            )

            insights.append(
                f"🔗 **{column1}** and "
                f"**{column2}** have a moderate "
                f"{direction} correlation "
                f"({value:.2f})."
            )

    return insights