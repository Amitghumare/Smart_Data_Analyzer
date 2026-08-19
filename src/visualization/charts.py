import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# COLUMN HELPERS
# ============================================================

def get_numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def get_categorical_columns(df):

    return df.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    ).columns.tolist()


def get_datetime_columns(df):

    return df.select_dtypes(
        include=[
            "datetime64[ns]",
            "datetime64[ns, UTC]"
        ]
    ).columns.tolist()


# ============================================================
# CLEAN DATA FOR PLOT
# ============================================================

def clean_plot_data(
    df,
    columns
):

    columns = [
        column
        for column in columns
        if column in df.columns
    ]

    if not columns:

        return pd.DataFrame()

    return (
        df[columns]
        .dropna()
        .copy()
    )


# ============================================================
# LINE CHART
# ============================================================

def create_line_chart(
    df,
    x_column,
    y_column,
    title=None
):

    plot_df = clean_plot_data(
        df,
        [
            x_column,
            y_column
        ]
    )

    if plot_df.empty:

        return None

    # Sort by X column
    try:

        plot_df = plot_df.sort_values(
            by=x_column
        )

    except Exception:

        pass

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.plot(
        plot_df[x_column],
        plot_df[y_column]
    )

    ax.set_title(
        title
        or f"{y_column} vs {x_column}"
    )

    ax.set_xlabel(
        x_column
    )

    ax.set_ylabel(
        y_column
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    return fig


# ============================================================
# BAR CHART
# ============================================================

def create_bar_chart(
    df,
    x_column,
    y_column,
    aggregation="mean",
    title=None
):

    plot_df = clean_plot_data(
        df,
        [
            x_column,
            y_column
        ]
    )

    if plot_df.empty:

        return None

    grouped = (
        plot_df
        .groupby(
            x_column
        )[y_column]
        .agg(aggregation)
        .sort_values(
            ascending=False
        )
        .head(20)
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.bar(
        grouped.index.astype(str),
        grouped.values
    )

    ax.set_title(
        title
        or f"{aggregation.title()} "
           f"{y_column} by {x_column}"
    )

    ax.set_xlabel(
        x_column
    )

    ax.set_ylabel(
        f"{aggregation.title()} "
        f"{y_column}"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    return fig


# ============================================================
# HORIZONTAL BAR CHART
# ============================================================

def create_horizontal_bar_chart(
    df,
    x_column,
    y_column,
    aggregation="mean",
    title=None
):

    plot_df = clean_plot_data(
        df,
        [
            x_column,
            y_column
        ]
    )

    if plot_df.empty:

        return None

    grouped = (
        plot_df
        .groupby(
            x_column
        )[y_column]
        .agg(aggregation)
        .sort_values(
            ascending=True
        )
        .tail(20)
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.barh(
        grouped.index.astype(str),
        grouped.values
    )

    ax.set_title(
        title
        or f"{aggregation.title()} "
           f"{y_column} by {x_column}"
    )

    ax.set_xlabel(
        f"{aggregation.title()} "
        f"{y_column}"
    )

    ax.set_ylabel(
        x_column
    )

    plt.tight_layout()

    return fig


# ============================================================
# SCATTER PLOT
# ============================================================

def create_scatter_plot(
    df,
    x_column,
    y_column,
    title=None
):

    plot_df = clean_plot_data(
        df,
        [
            x_column,
            y_column
        ]
    )

    if plot_df.empty:

        return None

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.scatter(
        plot_df[x_column],
        plot_df[y_column],
        alpha=0.6
    )

    ax.set_title(
        title
        or f"{x_column} vs {y_column}"
    )

    ax.set_xlabel(
        x_column
    )

    ax.set_ylabel(
        y_column
    )

    plt.tight_layout()

    return fig


# ============================================================
# HISTOGRAM
# ============================================================

def create_histogram(
    df,
    column,
    bins=30,
    title=None
):

    if column not in df.columns:

        return None

    series = (
        df[column]
        .dropna()
    )

    if series.empty:

        return None

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.hist(
        series,
        bins=bins
    )

    ax.set_title(
        title
        or f"Distribution of {column}"
    )

    ax.set_xlabel(
        column
    )

    ax.set_ylabel(
        "Frequency"
    )

    plt.tight_layout()

    return fig


# ============================================================
# BOX PLOT
# ============================================================

def create_box_plot(
    df,
    column,
    title=None
):

    if column not in df.columns:

        return None

    series = (
        df[column]
        .dropna()
    )

    if series.empty:

        return None

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.boxplot(
        series
    )

    ax.set_title(
        title
        or f"Box Plot of {column}"
    )

    ax.set_ylabel(
        column
    )

    plt.tight_layout()

    return fig


# ============================================================
# PIE CHART
# ============================================================

def create_pie_chart(
    df,
    column,
    top_n=10,
    title=None
):

    if column not in df.columns:

        return None

    counts = (
        df[column]
        .value_counts(
            dropna=False
        )
        .head(top_n)
    )

    if counts.empty:

        return None

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    ax.pie(
        counts.values,
        labels=counts.index.astype(str),
        autopct="%1.1f%%"
    )

    ax.set_title(
        title
        or f"Distribution of {column}"
    )

    plt.tight_layout()

    return fig


# ============================================================
# COUNT PLOT
# ============================================================

def create_count_plot(
    df,
    column,
    top_n=20,
    title=None
):

    if column not in df.columns:

        return None

    counts = (
        df[column]
        .value_counts(
            dropna=False
        )
        .head(top_n)
    )

    if counts.empty:

        return None

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.bar(
        counts.index.astype(str),
        counts.values
    )

    ax.set_title(
        title
        or f"Count of {column}"
    )

    ax.set_xlabel(
        column
    )

    ax.set_ylabel(
        "Count"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    return fig


# ============================================================
# AREA CHART
# ============================================================

def create_area_chart(
    df,
    x_column,
    y_column,
    title=None
):

    plot_df = clean_plot_data(
        df,
        [
            x_column,
            y_column
        ]
    )

    if plot_df.empty:

        return None

    try:

        plot_df = plot_df.sort_values(
            by=x_column
        )

    except Exception:

        pass

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.fill_between(
        range(len(plot_df)),
        plot_df[y_column].values
    )

    ax.set_title(
        title
        or f"Area Chart: {y_column}"
    )

    ax.set_xlabel(
        x_column
    )

    ax.set_ylabel(
        y_column
    )

    if len(plot_df) <= 20:

        ax.set_xticks(
            range(len(plot_df))
        )

        ax.set_xticklabels(
            plot_df[x_column]
            .astype(str),
            rotation=45,
            ha="right"
        )

    plt.tight_layout()

    return fig


# ============================================================
# CORRELATION HEATMAP
# ============================================================

def create_correlation_heatmap(
    df,
    title="Correlation Heatmap"
):

    numeric_df = (
        df.select_dtypes(
            include=np.number
        )
    )

    if numeric_df.shape[1] < 2:

        return None

    correlation = (
        numeric_df
        .corr(
            numeric_only=True
        )
    )

    fig, ax = plt.subplots(
        figsize=(10, 8)
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
        title
    )

    for i in range(
        len(correlation.columns)
    ):

        for j in range(
            len(correlation.columns)
        ):

            ax.text(
                j,
                i,
                f"{correlation.iloc[i, j]:.2f}",
                ha="center",
                va="center"
            )

    plt.colorbar(
        image,
        ax=ax
    )

    plt.tight_layout()

    return fig


# ============================================================
# SAVE FIGURE TO BYTES
# ============================================================

def figure_to_bytes(
    fig,
    format="png"
):

    from io import BytesIO

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format=format,
        dpi=300,
        bbox_inches="tight"
    )

    buffer.seek(0)

    return buffer.getvalue()