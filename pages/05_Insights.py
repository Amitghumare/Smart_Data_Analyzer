import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Insights",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "dataset" not in st.session_state:
    st.session_state["dataset"] = None

if "cleaned_data" not in st.session_state:
    st.session_state["cleaned_data"] = None

if "file_name" not in st.session_state:
    st.session_state["file_name"] = None


# ============================================================
# TITLE
# ============================================================

st.title("🧠 Data Insights")

st.markdown(
    """
    Automatically discover important patterns, trends,
    relationships, missing values, outliers, and key
    statistical findings from your dataset.
    """
)


# ============================================================
# LOAD DATASET
# ============================================================

dataset = st.session_state.get("dataset")

cleaned_data = st.session_state.get("cleaned_data")


# ------------------------------------------------------------
# USE CLEANED DATA
# ------------------------------------------------------------

if (
    cleaned_data is not None
    and isinstance(cleaned_data, pd.DataFrame)
    and not cleaned_data.empty
):

    df = cleaned_data.copy()

    st.success("✅ Using the cleaned dataset.")


# ------------------------------------------------------------
# USE ORIGINAL DATA
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

    st.warning(
        "⚠️ Please upload a dataset first."
    )

    st.info(
        "Go to the Upload Dataset page and upload "
        "a CSV or Excel file."
    )

    if st.button(
        "📤 Go to Upload Dataset",
        type="primary",
        use_container_width=True,
        key="insights_upload_button"
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
# OVERVIEW
# ============================================================

st.divider()

st.header("📊 Dataset Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Rows",
        f"{len(df):,}"
    )


with col2:

    st.metric(
        "Columns",
        f"{len(df.columns):,}"
    )


with col3:

    missing_count = int(
        df.isnull()
        .sum()
        .sum()
    )

    st.metric(
        "Missing Values",
        f"{missing_count:,}"
    )


with col4:

    duplicate_count = int(
        df.duplicated()
        .sum()
    )

    st.metric(
        "Duplicates",
        f"{duplicate_count:,}"
    )


# ============================================================
# AUTOMATIC DATASET INSIGHTS
# ============================================================

st.divider()

st.header("💡 Automatic Insights")


insights = []


# ------------------------------------------------------------
# DATASET SIZE
# ------------------------------------------------------------

insights.append(
    f"Your dataset contains **{len(df):,} rows** "
    f"and **{len(df.columns):,} columns**."
)


# ------------------------------------------------------------
# NUMERICAL / CATEGORICAL
# ------------------------------------------------------------

insights.append(
    f"The dataset contains **{len(numeric_columns)} "
    f"numerical columns** and "
    f"**{len(categorical_columns)} categorical columns**."
)


# ------------------------------------------------------------
# MISSING VALUES
# ------------------------------------------------------------

missing_total = int(
    df.isnull()
    .sum()
    .sum()
)


if missing_total == 0:

    insights.append(
        "✅ The dataset contains **no missing values**."
    )

else:

    missing_percent = (
        missing_total
        /
        (df.shape[0] * df.shape[1])
    ) * 100

    insights.append(
        f"⚠️ The dataset contains **{missing_total:,} "
        f"missing values**, representing approximately "
        f"**{missing_percent:.2f}%** of all cells."
    )


# ------------------------------------------------------------
# DUPLICATES
# ------------------------------------------------------------

duplicate_total = int(
    df.duplicated()
    .sum()
)


if duplicate_total == 0:

    insights.append(
        "✅ No duplicate rows were detected."
    )

else:

    insights.append(
        f"⚠️ **{duplicate_total:,} duplicate rows** "
        "were detected."
    )


# ------------------------------------------------------------
# DISPLAY BASIC INSIGHTS
# ------------------------------------------------------------

for insight in insights:

    st.info(
        insight
    )


# ============================================================
# NUMERICAL COLUMN INSIGHTS
# ============================================================

st.divider()

st.header("🔢 Numerical Insights")


if numeric_columns:

    numerical_insights = []


    for column in numeric_columns:

        series = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()


        if series.empty:
            continue


        mean_value = series.mean()

        median_value = series.median()

        min_value = series.min()

        max_value = series.max()


        # ----------------------------------------------------
        # OUTLIERS
        # ----------------------------------------------------

        q1 = series.quantile(
            0.25
        )

        q3 = series.quantile(
            0.75
        )

        iqr = q3 - q1


        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )


        outlier_count = int(
            (
                (series < lower_bound)
                |
                (series > upper_bound)
            ).sum()
        )


        numerical_insights.append({

            "Column":
                column,

            "Mean":
                round(
                    mean_value,
                    2
                ),

            "Median":
                round(
                    median_value,
                    2
                ),

            "Minimum":
                round(
                    min_value,
                    2
                ),

            "Maximum":
                round(
                    max_value,
                    2
                ),

            "Outliers":
                outlier_count

        })


    if numerical_insights:

        numerical_df = pd.DataFrame(
            numerical_insights
        )


        st.dataframe(
            numerical_df,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # HIGHEST MEAN
        # ----------------------------------------------------

        highest_mean_row = (
            numerical_df
            .sort_values(
                "Mean",
                ascending=False
            )
            .iloc[0]
        )


        st.info(
            f"📌 **{highest_mean_row['Column']}** "
            f"has the highest average value among "
            f"the numerical columns "
            f"({highest_mean_row['Mean']:,.2f})."
        )


else:

    st.info(
        "No numerical columns available."
    )


# ============================================================
# CATEGORICAL INSIGHTS
# ============================================================

st.divider()

st.header("🏷️ Categorical Insights")


if categorical_columns:

    selected_category = st.selectbox(
        "Select a categorical column",
        categorical_columns,
        key="insights_category"
    )


    category_counts = (
        df[selected_category]
        .value_counts(
            dropna=False
        )
    )


    if not category_counts.empty:

        top_category = (
            category_counts
            .index[0]
        )

        top_count = int(
            category_counts.iloc[0]
        )


        total_values = (
            category_counts.sum()
        )


        percentage = (
            top_count
            /
            total_values
        ) * 100


        st.success(
            f"🏆 The most common value in "
            f"**{selected_category}** is "
            f"**{top_category}**, appearing "
            f"**{top_count:,} times "
            f"({percentage:.2f}%)**."
        )


        st.subheader(
            "Frequency Distribution"
        )


        category_display = pd.DataFrame({

            "Category":
                category_counts
                .head(15)
                .index
                .astype(str),

            "Count":
                category_counts
                .head(15)
                .values

        })


        st.dataframe(
            category_display,
            use_container_width=True,
            hide_index=True
        )


else:

    st.info(
        "No categorical columns available."
    )


# ============================================================
# CORRELATION INSIGHTS
# ============================================================

st.divider()

st.header("🔗 Relationship Insights")


if len(numeric_columns) >= 2:

    correlation_matrix = (
        df[numeric_columns]
        .corr()
    )


    correlation_pairs = []


    for i in range(
        len(correlation_matrix.columns)
    ):

        for j in range(
            i + 1,
            len(correlation_matrix.columns)
        ):

            column_1 = (
                correlation_matrix.columns[i]
            )

            column_2 = (
                correlation_matrix.columns[j]
            )


            value = (
                correlation_matrix
                .iloc[i, j]
            )


            if not pd.isna(value):

                correlation_pairs.append({

                    "Column 1":
                        column_1,

                    "Column 2":
                        column_2,

                    "Correlation":
                        round(
                            value,
                            3
                        ),

                    "Absolute":
                        abs(value)

                })


    if correlation_pairs:

        correlation_df = pd.DataFrame(
            correlation_pairs
        )


        correlation_df = (
            correlation_df
            .sort_values(
                "Absolute",
                ascending=False
            )
        )


        # ----------------------------------------------------
        # STRONGEST RELATIONSHIP
        # ----------------------------------------------------

        strongest = (
            correlation_df
            .iloc[0]
        )


        strongest_value = (
            strongest["Correlation"]
        )


        if abs(strongest_value) >= 0.7:

            strength = "strong"

        elif abs(strongest_value) >= 0.4:

            strength = "moderate"

        else:

            strength = "weak"


        if strongest_value > 0:

            direction = "positive"

        else:

            direction = "negative"


        st.success(
            f"🔗 The strongest relationship is between "
            f"**{strongest['Column 1']}** and "
            f"**{strongest['Column 2']}** with a "
            f"**{strength} {direction} correlation** "
            f"of **{strongest_value:.3f}**."
        )


        st.subheader(
            "Top Relationships"
        )


        display_corr = (
            correlation_df
            .drop(
                columns=["Absolute"]
            )
            .head(10)
        )


        st.dataframe(
            display_corr,
            use_container_width=True,
            hide_index=True
        )


else:

    st.info(
        "At least two numerical columns "
        "are required."
    )


# ============================================================
# OUTLIER INSIGHTS
# ============================================================

st.divider()

st.header("🚨 Outlier Insights")


if numeric_columns:

    outlier_results = []


    for column in numeric_columns:

        series = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()


        if series.empty:
            continue


        q1 = series.quantile(
            0.25
        )

        q3 = series.quantile(
            0.75
        )

        iqr = q3 - q1


        lower = (
            q1 - 1.5 * iqr
        )

        upper = (
            q3 + 1.5 * iqr
        )


        count = int(
            (
                (series < lower)
                |
                (series > upper)
            ).sum()
        )


        percentage = (
            count
            /
            len(series)
        ) * 100


        outlier_results.append({

            "Column":
                column,

            "Outliers":
                count,

            "Outlier %":
                round(
                    percentage,
                    2
                )

        })


    outlier_df = pd.DataFrame(
        outlier_results
    )


    if not outlier_df.empty:

        outlier_df = (
            outlier_df
            .sort_values(
                "Outliers",
                ascending=False
            )
        )


        st.dataframe(
            outlier_df,
            use_container_width=True,
            hide_index=True
        )


        highest_outlier = (
            outlier_df.iloc[0]
        )


        if highest_outlier["Outliers"] > 0:

            st.warning(
                f"⚠️ **{highest_outlier['Column']}** "
                f"contains the highest number of "
                f"detected outliers: "
                f"**{int(highest_outlier['Outliers']):,}**."
            )

        else:

            st.success(
                "✅ No statistical outliers were detected."
            )


else:

    st.info(
        "No numerical columns available."
    )


# ============================================================
# TOP/BOTTOM VALUES
# ============================================================

st.divider()

st.header("📌 Important Numerical Values")


if numeric_columns:

    selected_column = st.selectbox(
        "Select a numerical column",
        numeric_columns,
        key="insights_top_bottom_column"
    )


    series = pd.to_numeric(
        df[selected_column],
        errors="coerce"
    ).dropna()


    if not series.empty:

        col1, col2 = st.columns(2)


        with col1:

            st.subheader(
                "🔝 Highest Values"
            )


            highest_values = (
                series
                .nlargest(10)
                .reset_index(drop=True)
            )


            highest_df = pd.DataFrame({

                "Rank":
                    range(
                        1,
                        len(highest_values) + 1
                    ),

                "Value":
                    highest_values

            })


            st.dataframe(
                highest_df,
                use_container_width=True,
                hide_index=True
            )


        with col2:

            st.subheader(
                "🔻 Lowest Values"
            )


            lowest_values = (
                series
                .nsmallest(10)
                .reset_index(drop=True)
            )


            lowest_df = pd.DataFrame({

                "Rank":
                    range(
                        1,
                        len(lowest_values) + 1
                    ),

                "Value":
                    lowest_values

            })


            st.dataframe(
                lowest_df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.divider()

st.header("📋 Executive Summary")


summary_points = []


summary_points.append(
    f"The dataset contains "
    f"{len(df):,} records across "
    f"{len(df.columns):,} variables."
)


if missing_total == 0:

    summary_points.append(
        "The dataset has no missing values."
    )

else:

    summary_points.append(
        f"There are {missing_total:,} missing values "
        "that may require further treatment."
    )


if duplicate_total == 0:

    summary_points.append(
        "No duplicate records were detected."
    )

else:

    summary_points.append(
        f"{duplicate_total:,} duplicate records "
        "were detected."
    )


if numeric_columns:

    summary_points.append(
        f"{len(numeric_columns)} numerical variables "
        "are available for quantitative analysis."
    )


if categorical_columns:

    summary_points.append(
        f"{len(categorical_columns)} categorical "
        "variables are available for segmentation "
        "and frequency analysis."
    )


for i, point in enumerate(
    summary_points,
    start=1
):

    st.write(
        f"**{i}.** {point}"
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
        "⬅️ Previous: Visualization",
        use_container_width=True,
        key="insights_previous_visualization"
    ):

        st.switch_page(
            "pages/04_Visualization.py"
        )


# ------------------------------------------------------------
# NEXT
# ------------------------------------------------------------

with col2:

    if st.button(
        "Next: Reports ➡️",
        type="primary",
        use_container_width=True,
        key="insights_next_reports"
    ):

        st.switch_page(
            "pages/06_Reports.py"
        )