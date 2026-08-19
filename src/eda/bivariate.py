import pandas as pd
import matplotlib.pyplot as plt


def numerical_bivariate(
    df,
    x_column,
    y_column
):

    data = df[
        [x_column, y_column]
    ].copy()

    data[x_column] = pd.to_numeric(
        data[x_column],
        errors="coerce"
    )

    data[y_column] = pd.to_numeric(
        data[y_column],
        errors="coerce"
    )

    data = data.dropna()

    if data.empty:
        return None

    fig, ax = plt.subplots()

    ax.scatter(
        data[x_column],
        data[y_column],
        alpha=0.6
    )

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)

    ax.set_title(
        f"{x_column} vs {y_column}"
    )

    return fig


def categorical_numerical(
    df,
    categorical_column,
    numerical_column
):

    data = df[
        [
            categorical_column,
            numerical_column
        ]
    ].copy()

    data[numerical_column] = pd.to_numeric(
        data[numerical_column],
        errors="coerce"
    )

    data = data.dropna()

    if data.empty:
        return None

    grouped = (
        data
        .groupby(categorical_column)[numerical_column]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(15)
    )

    fig, ax = plt.subplots()

    grouped.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        f"Average {numerical_column} by "
        f"{categorical_column}"
    )

    ax.set_xlabel(
        categorical_column
    )

    ax.set_ylabel(
        f"Average {numerical_column}"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    return fig