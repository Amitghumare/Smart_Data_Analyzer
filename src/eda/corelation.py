import matplotlib.pyplot as plt


def correlation_matrix(df):

    numeric_df = (
        df
        .select_dtypes(
            include="number"
        )
    )

    if numeric_df.shape[1] < 2:
        return None

    correlation = (
        numeric_df
        .corr()
    )

    fig, ax = plt.subplots(
        figsize=(10, 7)
    )

    image = ax.imshow(
        correlation,
        aspect="auto"
    )

    ax.set_xticks(
        range(
            len(correlation.columns)
        )
    )

    ax.set_yticks(
        range(
            len(correlation.columns)
        )
    )

    ax.set_xticklabels(
        correlation.columns,
        rotation=45,
        ha="right"
    )

    ax.set_yticklabels(
        correlation.columns
    )

    ax.set_title(
        "Correlation Matrix"
    )

    fig.colorbar(
        image,
        ax=ax
    )

    return fig, correlation