def categorical_insights(df):

    insights = []

    categorical_columns = (
        df
        .select_dtypes(
            include=[
                "object",
                "category"
            ]
        )
        .columns
        .tolist()
    )

    for column in categorical_columns:

        data = df[column].dropna()

        if data.empty:
            continue

        unique_count = data.nunique()

        # ------------------------------------------
        # Unique values
        # ------------------------------------------

        insights.append(
            f"🔤 **{column}** contains "
            f"{unique_count} unique categories."
        )

        # ------------------------------------------
        # Most common category
        # ------------------------------------------

        counts = data.value_counts()

        if not counts.empty:

            top_category = counts.index[0]
            top_count = counts.iloc[0]

            percentage = (
                top_count
                / len(data)
                * 100
            )

            insights.append(
                f"🏆 **{top_category}** is the most "
                f"frequent value in **{column}**, "
                f"appearing in {percentage:.1f}% "
                f"of records."
            )

        # ------------------------------------------
        # High cardinality
        # ------------------------------------------

        if unique_count > 50:

            insights.append(
                f"⚠️ **{column}** has high "
                f"cardinality with "
                f"{unique_count} unique values."
            )

    return insights