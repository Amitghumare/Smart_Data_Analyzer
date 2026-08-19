import pandas as pd
import matplotlib.pyplot as plt


def numerical_summary(df, column):

    data = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if data.empty:
        return None

    summary = {
        "Count": int(data.count()),
        "Mean": float(data.mean()),
        "Median": float(data.median()),
        "Standard Deviation": float(data.std()),
        "Minimum": float(data.min()),
        "Maximum": float(data.max()),
        "25th Percentile": float(data.quantile(0.25)),
        "75th Percentile": float(data.quantile(0.75))
    }

    return summary


def plot_histogram(df, column):

    data = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    fig, ax = plt.subplots()

    ax.hist(
        data,
        bins=30
    )

    ax.set_title(
        f"Distribution of {column}"
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    return fig


def plot_boxplot(df, column):

    data = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    fig, ax = plt.subplots()

    ax.boxplot(data)

    ax.set_title(
        f"Boxplot of {column}"
    )

    ax.set_ylabel(column)

    return fig


def categorical_summary(df, column):

    data = df[column].dropna()

    if data.empty:
        return None

    summary = (
        data
        .value_counts()
        .reset_index()
    )

    summary.columns = [
        "Category",
        "Count"
    ]

    summary["Percentage"] = (
        summary["Count"]
        / summary["Count"].sum()
        * 100
    ).round(2)

    return summary

