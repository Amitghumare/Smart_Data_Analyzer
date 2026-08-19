def calculate_quality_score(
    df
):

    if df.empty:

        return 0


    total_cells = (
        df.shape[0]
        * df.shape[1]
    )

    if total_cells == 0:

        return 0


    missing_cells = (
        df.isnull()
        .sum()
        .sum()
    )

    duplicate_rows = (
        df.duplicated()
        .sum()
    )


    missing_penalty = (
        missing_cells
        / total_cells
    ) * 50


    duplicate_penalty = (
        duplicate_rows
        / len(df)
    ) * 30


    score = (
        100
        - missing_penalty
        - duplicate_penalty
    )


    score = max(
        0,
        min(
            100,
            score
        )
    )


    return round(
        score,
        2
    )