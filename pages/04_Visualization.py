import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Visualization",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "dataset" not in st.session_state:
    st.session_state["dataset"] = None

if "cleaned_data" not in st.session_state:
    st.session_state["cleaned_data"] = None


# ============================================================
# TITLE
# ============================================================

st.title("📊 Data Visualization")

st.markdown(
    """
    Create interactive visualizations from your dataset.
    Choose the chart type, select columns, and generate
    charts for your analysis.
    """
)


# ============================================================
# LOAD DATASET
# ============================================================

dataset = st.session_state.get("dataset")

cleaned_data = st.session_state.get("cleaned_data")


# ------------------------------------------------------------
# USE CLEANED DATA FIRST
# ------------------------------------------------------------

if (
    cleaned_data is not None
    and isinstance(cleaned_data, pd.DataFrame)
    and not cleaned_data.empty
):

    df = cleaned_data.copy()

    st.success("✅ Using the cleaned dataset.")


# ------------------------------------------------------------
# OTHERWISE USE ORIGINAL DATA
# ------------------------------------------------------------

elif (
    dataset is not None
    and isinstance(dataset, pd.DataFrame)
    and not dataset.empty
):

    df = dataset.copy()

    st.info("ℹ️ Using the original dataset.")


# ------------------------------------------------------------
# NO DATASET
# ------------------------------------------------------------

else:

    st.warning("⚠️ Please upload a dataset first.")

    st.info(
        "Go to the Upload Dataset page and upload "
        "a CSV or Excel file."
    )

    if st.button(
        "📤 Go to Upload Dataset",
        type="primary",
        use_container_width=True,
        key="visualization_go_upload"
    ):

        st.switch_page(
            "pages/01_Upload.py"
        )

    st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.divider()

st.subheader("📊 Dataset Information")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )

with col2:

    st.metric(
        "Columns",
        f"{df.shape[1]:,}"
    )

with col3:

    st.metric(
        "Numerical Columns",
        len(
            df.select_dtypes(
                include=np.number
            ).columns
        )
    )

with col4:

    st.metric(
        "Categorical Columns",
        len(
            df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            ).columns
        )
    )


# ============================================================
# COLUMN TYPES
# ============================================================

numeric_columns = (
    df.select_dtypes(
        include=np.number
    )
    .columns
    .tolist()
)

categorical_columns = (
    df.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    )
    .columns
    .tolist()
)


# ============================================================
# VISUALIZATION SETTINGS
# ============================================================

st.divider()

st.header("🎨 Create Visualization")


chart_type = st.selectbox(
    "Select Chart Type",
    [
        "📊 Bar Chart",
        "📈 Line Chart",
        "🔵 Scatter Plot",
        "📉 Histogram",
        "🥧 Pie Chart",
        "📦 Box Plot",
        "🔥 Correlation Heatmap"
    ],
    key="visualization_chart_type"
)


# ============================================================
# BAR CHART
# ============================================================

if chart_type == "📊 Bar Chart":

    st.subheader("📊 Bar Chart")


    if not categorical_columns:

        st.warning(
            "No categorical columns available "
            "for a bar chart."
        )

    elif not numeric_columns:

        st.warning(
            "No numerical columns available."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            x_column = st.selectbox(
                "Select Category",
                categorical_columns,
                key="bar_x_column"
            )


        with col2:

            y_column = st.selectbox(
                "Select Numerical Value",
                numeric_columns,
                key="bar_y_column"
            )


        aggregation = st.selectbox(
            "Aggregation",
            [
                "Sum",
                "Mean",
                "Count",
                "Median"
            ],
            key="bar_aggregation"
        )


        plot_df = df[
            [x_column, y_column]
        ].copy()


        plot_df[y_column] = pd.to_numeric(
            plot_df[y_column],
            errors="coerce"
        )


        plot_df = plot_df.dropna(
            subset=[x_column]
        )


        if aggregation == "Sum":

            result = (
                plot_df
                .groupby(x_column)[y_column]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(20)
            )


        elif aggregation == "Mean":

            result = (
                plot_df
                .groupby(x_column)[y_column]
                .mean()
                .sort_values(
                    ascending=False
                )
                .head(20)
            )


        elif aggregation == "Median":

            result = (
                plot_df
                .groupby(x_column)[y_column]
                .median()
                .sort_values(
                    ascending=False
                )
                .head(20)
            )


        else:

            result = (
                plot_df
                .groupby(x_column)[y_column]
                .count()
                .sort_values(
                    ascending=False
                )
                .head(20)
            )


        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        result.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel(
            x_column
        )

        ax.set_ylabel(
            y_column
        )

        ax.set_title(
            f"{aggregation} of {y_column} by {x_column}"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        st.pyplot(
            fig,
            clear_figure=True
        )

        plt.close(fig)


# ============================================================
# LINE CHART
# ============================================================

elif chart_type == "📈 Line Chart":

    st.subheader("📈 Line Chart")


    if len(numeric_columns) < 1:

        st.warning(
            "No numerical columns available."
        )

    else:

        x_options = df.columns.tolist()

        x_column = st.selectbox(
            "Select X-axis",
            x_options,
            key="line_x_column"
        )


        y_column = st.selectbox(
            "Select Y-axis",
            numeric_columns,
            key="line_y_column"
        )


        plot_df = df[
            [x_column, y_column]
        ].copy()


        plot_df[y_column] = pd.to_numeric(
            plot_df[y_column],
            errors="coerce"
        )


        plot_df = plot_df.dropna()


        if not plot_df.empty:

            # Sort by X when possible
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


            ax.set_xlabel(
                x_column
            )

            ax.set_ylabel(
                y_column
            )

            ax.set_title(
                f"{y_column} over {x_column}"
            )


            plt.xticks(
                rotation=45,
                ha="right"
            )

            plt.tight_layout()


            st.pyplot(
                fig,
                clear_figure=True
            )

            plt.close(fig)


# ============================================================
# SCATTER PLOT
# ============================================================

elif chart_type == "🔵 Scatter Plot":

    st.subheader("🔵 Scatter Plot")


    if len(numeric_columns) < 2:

        st.warning(
            "At least two numerical columns "
            "are required."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            x_column = st.selectbox(
                "Select X-axis",
                numeric_columns,
                key="scatter_x_column"
            )


        with col2:

            y_column = st.selectbox(
                "Select Y-axis",
                numeric_columns,
                index=(
                    1
                    if len(numeric_columns) > 1
                    else 0
                ),
                key="scatter_y_column"
            )


        plot_df = df[
            [x_column, y_column]
        ].copy()


        plot_df[x_column] = pd.to_numeric(
            plot_df[x_column],
            errors="coerce"
        )

        plot_df[y_column] = pd.to_numeric(
            plot_df[y_column],
            errors="coerce"
        )


        plot_df = plot_df.dropna()


        fig, ax = plt.subplots(
            figsize=(10, 6)
        )


        ax.scatter(
            plot_df[x_column],
            plot_df[y_column],
            alpha=0.6
        )


        ax.set_xlabel(
            x_column
        )

        ax.set_ylabel(
            y_column
        )

        ax.set_title(
            f"{x_column} vs {y_column}"
        )


        plt.tight_layout()


        st.pyplot(
            fig,
            clear_figure=True
        )

        plt.close(fig)


# ============================================================
# HISTOGRAM
# ============================================================

elif chart_type == "📉 Histogram":

    st.subheader("📉 Histogram")


    if not numeric_columns:

        st.warning(
            "No numerical columns available."
        )

    else:

        column = st.selectbox(
            "Select Column",
            numeric_columns,
            key="histogram_column"
        )


        bins = st.slider(
            "Number of Bins",
            min_value=5,
            max_value=100,
            value=30,
            key="histogram_bins"
        )


        series = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()


        fig, ax = plt.subplots(
            figsize=(10, 6)
        )


        ax.hist(
            series,
            bins=bins
        )


        ax.set_xlabel(
            column
        )

        ax.set_ylabel(
            "Frequency"
        )

        ax.set_title(
            f"Distribution of {column}"
        )


        plt.tight_layout()


        st.pyplot(
            fig,
            clear_figure=True
        )

        plt.close(fig)


# ============================================================
# PIE CHART
# ============================================================

elif chart_type == "🥧 Pie Chart":

    st.subheader("🥧 Pie Chart")


    if not categorical_columns:

        st.warning(
            "No categorical columns available."
        )

    else:

        column = st.selectbox(
            "Select Category",
            categorical_columns,
            key="pie_column"
        )


        max_categories = st.slider(
            "Number of Categories",
            min_value=2,
            max_value=15,
            value=8,
            key="pie_categories"
        )


        counts = (
            df[column]
            .value_counts()
            .head(max_categories)
        )


        fig, ax = plt.subplots(
            figsize=(8, 8)
        )


        ax.pie(
            counts.values,
            labels=counts.index.astype(str),
            autopct="%1.1f%%"
        )


        ax.set_title(
            f"Distribution of {column}"
        )


        st.pyplot(
            fig,
            clear_figure=True
        )

        plt.close(fig)


# ============================================================
# BOX PLOT
# ============================================================

elif chart_type == "📦 Box Plot":

    st.subheader("📦 Box Plot")


    if not numeric_columns:

        st.warning(
            "No numerical columns available."
        )

    else:

        column = st.selectbox(
            "Select Numerical Column",
            numeric_columns,
            key="boxplot_column"
        )


        series = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()


        fig, ax = plt.subplots(
            figsize=(10, 5)
        )


        ax.boxplot(
            series,
            vert=False
        )


        ax.set_xlabel(
            column
        )

        ax.set_title(
            f"Box Plot of {column}"
        )


        plt.tight_layout()


        st.pyplot(
            fig,
            clear_figure=True
        )

        plt.close(fig)


# ============================================================
# CORRELATION HEATMAP
# ============================================================

elif chart_type == "🔥 Correlation Heatmap":

    st.subheader("🔥 Correlation Heatmap")


    if len(numeric_columns) < 2:

        st.warning(
            "At least two numerical columns "
            "are required."
        )

    else:

        correlation = (
            df[numeric_columns]
            .corr()
        )


        fig, ax = plt.subplots(
            figsize=(12, 8)
        )


        image = ax.imshow(
            correlation,
            interpolation="nearest",
            aspect="auto"
        )


        ax.set_xticks(
            range(len(correlation.columns))
        )

        ax.set_yticks(
            range(len(correlation.columns))
        )


        ax.set_xticklabels(
            correlation.columns,
            rotation=45,
            ha="right"
        )

        ax.set_yticklabels(
            correlation.columns
        )


        # Add correlation values
        for i in range(
            len(correlation.columns)
        ):

            for j in range(
                len(correlation.columns)
            ):

                value = correlation.iloc[
                    i,
                    j
                ]

                if not pd.isna(value):

                    ax.text(
                        j,
                        i,
                        f"{value:.2f}",
                        ha="center",
                        va="center"
                    )


        ax.set_title(
            "Correlation Matrix"
        )


        fig.colorbar(
            image,
            ax=ax
        )


        plt.tight_layout()


        st.pyplot(
            fig,
            clear_figure=True
        )

        plt.close(fig)


# ============================================================
# SAVE VISUALIZATION
# ============================================================

st.divider()

st.header("💾 Visualization")

st.info(
    "Use the chart controls above to explore "
    "different aspects of your dataset."
)


# ============================================================
# NAVIGATION
# ============================================================

st.divider()

st.header("🚀 Continue")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# PREVIOUS
# ------------------------------------------------------------

with col1:

    if st.button(
        "⬅️ Previous: EDA",
        use_container_width=True,
        key="visualization_previous_eda"
    ):

        st.switch_page(
            "pages/03_EDA.py"
        )


# ------------------------------------------------------------
# NEXT
# ------------------------------------------------------------

with col2:

    if st.button(
        "Next: Insights ➡️",
        type="primary",
        use_container_width=True,
        key="visualization_next_insights"
    ):

        st.switch_page(
            "pages/05_Insights.py"
        )