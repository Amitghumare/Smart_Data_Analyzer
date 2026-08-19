import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EDA",
    page_icon="🔍",
    layout="wide"
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "dataset" not in st.session_state:
    st.session_state["dataset"] = None

if "cleaned_data" not in st.session_state:
    st.session_state["cleaned_data"] = None

if "file_name" not in st.session_state:
    st.session_state["file_name"] = None


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🔍 Exploratory Data Analysis")

st.markdown(
    """
    Explore your dataset using statistical summaries,
    distributions, relationships, correlations,
    categorical analysis, missing values, and outliers.
    """
)


# ============================================================
# LOAD DATASET
# ============================================================

dataset = st.session_state.get("dataset")

cleaned_data = st.session_state.get("cleaned_data")


# ------------------------------------------------------------
# PRIORITY 1: CLEANED DATASET
# ------------------------------------------------------------

if (
    cleaned_data is not None
    and isinstance(cleaned_data, pd.DataFrame)
    and not cleaned_data.empty
):

    df = cleaned_data.copy()

    st.success(
        "✅ Using the cleaned dataset."
    )


# ------------------------------------------------------------
# PRIORITY 2: ORIGINAL DATASET
# ------------------------------------------------------------

elif (
    dataset is not None
    and isinstance(dataset, pd.DataFrame)
    and not dataset.empty
):

    df = dataset.copy()

    st.info(
        "ℹ️ Using the original dataset."
    )


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
        key="eda_upload_button"
    ):

        st.switch_page(
            "pages/01_Upload.py"
        )

    st.stop()


# ============================================================
# BASIC DATA PREPARATION
# ============================================================

# Remove completely empty rows only for analysis
analysis_df = df.copy()

# Make sure column names are strings
analysis_df.columns = (
    analysis_df.columns
    .astype(str)
    .str.strip()
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.divider()

st.header("📊 Dataset Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Rows",
        f"{analysis_df.shape[0]:,}"
    )


with col2:

    st.metric(
        "Columns",
        f"{analysis_df.shape[1]:,}"
    )


with col3:

    missing_values = int(
        analysis_df.isnull()
        .sum()
        .sum()
    )

    st.metric(
        "Missing Values",
        f"{missing_values:,}"
    )


with col4:

    duplicate_rows = int(
        analysis_df.duplicated()
        .sum()
    )

    st.metric(
        "Duplicate Rows",
        f"{duplicate_rows:,}"
    )


# ============================================================
# DATASET PREVIEW
# ============================================================

st.divider()

st.header("👀 Dataset Preview")

preview_rows = st.slider(
    "Number of rows to display",
    min_value=5,
    max_value=50,
    value=10,
    key="eda_preview_rows"
)


st.dataframe(
    analysis_df.head(preview_rows),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DATA TYPES
# ============================================================

st.divider()

st.header("📋 Column Information")


column_info = pd.DataFrame({
    "Column": analysis_df.columns,
    "Data Type": [
        str(analysis_df[col].dtype)
        for col in analysis_df.columns
    ],
    "Missing Values": [
        int(analysis_df[col].isnull().sum())
        for col in analysis_df.columns
    ],
    "Missing %": [
        round(
            analysis_df[col].isnull().mean() * 100,
            2
        )
        for col in analysis_df.columns
    ],
    "Unique Values": [
        int(analysis_df[col].nunique())
        for col in analysis_df.columns
    ]
})


st.dataframe(
    column_info,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# IDENTIFY COLUMN TYPES
# ============================================================

numeric_columns = (
    analysis_df
    .select_dtypes(include=np.number)
    .columns
    .tolist()
)


categorical_columns = (
    analysis_df
    .select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    )
    .columns
    .tolist()
)


date_columns = []

for column in analysis_df.columns:

    if (
        pd.api.types.is_datetime64_any_dtype(
            analysis_df[column]
        )
    ):

        date_columns.append(column)


# ============================================================
# COLUMN TYPE SUMMARY
# ============================================================

st.divider()

st.header("🧩 Column Type Summary")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Numerical Columns",
        len(numeric_columns)
    )


with col2:

    st.metric(
        "Categorical Columns",
        len(categorical_columns)
    )


with col3:

    st.metric(
        "Date Columns",
        len(date_columns)
    )


# ============================================================
# STATISTICAL SUMMARY
# ============================================================

st.divider()

st.header("📈 Statistical Summary")


if numeric_columns:

    statistics = (
        analysis_df[numeric_columns]
        .describe()
        .T
        .reset_index()
    )

    statistics = statistics.rename(
        columns={
            "index": "Column"
        }
    )

    st.dataframe(
        statistics,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No numerical columns available."
    )


# ============================================================
# UNIVARIATE ANALYSIS
# ============================================================

st.divider()

st.header("📊 Univariate Analysis")

st.write(
    "Analyze the distribution of individual numerical variables."
)


if numeric_columns:

    selected_univariate = st.selectbox(
        "Select a numerical column",
        numeric_columns,
        key="eda_univariate_column"
    )


    analysis_type = st.radio(
        "Choose visualization",
        [
            "Histogram",
            "Box Plot"
        ],
        horizontal=True,
        key="eda_univariate_type"
    )


    series = pd.to_numeric(
        analysis_df[selected_univariate],
        errors="coerce"
    ).dropna()


    if not series.empty:

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )


        if analysis_type == "Histogram":

            ax.hist(
                series,
                bins=30
            )

            ax.set_title(
                f"Distribution of {selected_univariate}"
            )

            ax.set_xlabel(
                selected_univariate
            )

            ax.set_ylabel(
                "Frequency"
            )


        else:

            ax.boxplot(
                series,
                vert=False
            )

            ax.set_title(
                f"Box Plot of {selected_univariate}"
            )

            ax.set_xlabel(
                selected_univariate
            )


        st.pyplot(
            fig,
            clear_figure=True
        )

        plt.close(fig)


        # ----------------------------------------------------
        # UNIVARIATE STATISTICS
        # ----------------------------------------------------

        st.subheader(
            "📌 Variable Statistics"
        )


        stat_col1, stat_col2, stat_col3, stat_col4 = (
            st.columns(4)
        )


        with stat_col1:

            st.metric(
                "Mean",
                f"{series.mean():,.2f}"
            )


        with stat_col2:

            st.metric(
                "Median",
                f"{series.median():,.2f}"
            )


        with stat_col3:

            st.metric(
                "Minimum",
                f"{series.min():,.2f}"
            )


        with stat_col4:

            st.metric(
                "Maximum",
                f"{series.max():,.2f}"
            )


else:

    st.info(
        "No numerical columns available "
        "for univariate analysis."
    )


# ============================================================
# CATEGORICAL ANALYSIS
# ============================================================

st.divider()

st.header("🏷️ Categorical Analysis")


if categorical_columns:

    selected_category = st.selectbox(
        "Select a categorical column",
        categorical_columns,
        key="eda_category_column"
    )


    category_counts = (
        analysis_df[selected_category]
        .value_counts(
            dropna=False
        )
        .head(20)
    )


    st.subheader(
        f"Frequency Distribution: {selected_category}"
    )


    st.bar_chart(
        category_counts
    )


    category_table = pd.DataFrame({
        "Category": category_counts.index.astype(str),
        "Count": category_counts.values
    })


    st.dataframe(
        category_table,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No categorical columns available."
    )


# ============================================================
# BIVARIATE ANALYSIS
# ============================================================

st.divider()

st.header("🔗 Bivariate Analysis")

st.write(
    "Analyze the relationship between two numerical variables."
)


if len(numeric_columns) >= 2:

    col1, col2 = st.columns(2)


    with col1:

        x_column = st.selectbox(
            "Select X-axis",
            numeric_columns,
            key="eda_bivariate_x"
        )


    with col2:

        default_index = 1

        if (
            default_index >= len(numeric_columns)
        ):

            default_index = 0


        y_column = st.selectbox(
            "Select Y-axis",
            numeric_columns,
            index=default_index,
            key="eda_bivariate_y"
        )


    if x_column == y_column:

        st.warning(
            "⚠️ Please select two different columns."
        )


    else:

        plot_df = analysis_df[
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


        if not plot_df.empty:

            fig, ax = plt.subplots(
                figsize=(10, 5)
            )


            ax.scatter(
                plot_df[x_column],
                plot_df[y_column],
                alpha=0.6
            )


            ax.set_title(
                f"{x_column} vs {y_column}"
            )

            ax.set_xlabel(
                x_column
            )

            ax.set_ylabel(
                y_column
            )


            st.pyplot(
                fig,
                clear_figure=True
            )

            plt.close(fig)


            # ------------------------------------------------
            # CORRELATION
            # ------------------------------------------------

            correlation_value = (
                plot_df[x_column]
                .corr(
                    plot_df[y_column]
                )
            )


            st.metric(
                "Correlation",
                f"{correlation_value:.3f}"
            )


        else:

            st.warning(
                "Not enough valid numerical data "
                "to create this analysis."
            )

else:

    st.info(
        "At least two numerical columns are "
        "required for bivariate analysis."
    )


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

st.divider()

st.header("🔥 Correlation Analysis")


if len(numeric_columns) >= 2:

    correlation_matrix = (
        analysis_df[numeric_columns]
        .corr()
    )


    st.subheader(
        "Correlation Matrix"
    )


    st.dataframe(
        correlation_matrix.round(3),
        use_container_width=True
    )


    # --------------------------------------------------------
    # FIND STRONGEST CORRELATIONS
    # --------------------------------------------------------

    correlation_pairs = []


    for i in range(
        len(correlation_matrix.columns)
    ):

        for j in range(
            i + 1,
            len(correlation_matrix.columns)
        ):

            col_a = correlation_matrix.columns[i]

            col_b = correlation_matrix.columns[j]

            correlation_value = (
                correlation_matrix.iloc[
                    i,
                    j
                ]
            )


            if not pd.isna(
                correlation_value
            ):

                correlation_pairs.append({

                    "Column 1":
                        col_a,

                    "Column 2":
                        col_b,

                    "Correlation":
                        round(
                            correlation_value,
                            3
                        ),

                    "Absolute Correlation":
                        abs(
                            correlation_value
                        )
                })


    if correlation_pairs:

        correlation_df = pd.DataFrame(
            correlation_pairs
        )


        correlation_df = (
            correlation_df
            .sort_values(
                "Absolute Correlation",
                ascending=False
            )
        )


        correlation_df = (
            correlation_df
            .drop(
                columns=[
                    "Absolute Correlation"
                ]
            )
        )


        st.subheader(
            "🔝 Strongest Relationships"
        )


        st.dataframe(
            correlation_df.head(10),
            use_container_width=True,
            hide_index=True
        )


else:

    st.info(
        "At least two numerical columns are "
        "required for correlation analysis."
    )


# ============================================================
# MISSING VALUE ANALYSIS
# ============================================================

st.divider()

st.header("❓ Missing Value Analysis")


missing_analysis = pd.DataFrame({

    "Column":
        analysis_df.columns,

    "Missing Values": [
        int(
            analysis_df[col]
            .isnull()
            .sum()
        )
        for col in analysis_df.columns
    ],

    "Missing %": [
        round(
            analysis_df[col]
            .isnull()
            .mean() * 100,
            2
        )
        for col in analysis_df.columns
    ]
})


missing_analysis = (
    missing_analysis[
        missing_analysis[
            "Missing Values"
        ] > 0
    ]
    .sort_values(
        "Missing Values",
        ascending=False
    )
)


if not missing_analysis.empty:

    st.dataframe(
        missing_analysis,
        use_container_width=True,
        hide_index=True
    )


    st.bar_chart(
        missing_analysis.set_index(
            "Column"
        )["Missing Values"]
    )


else:

    st.success(
        "✅ No missing values found."
    )


# ============================================================
# OUTLIER ANALYSIS
# ============================================================

st.divider()

st.header("🚨 Outlier Analysis")


if numeric_columns:

    outlier_column = st.selectbox(
        "Select numerical column",
        numeric_columns,
        key="eda_outlier_column"
    )


    outlier_series = pd.to_numeric(
        analysis_df[outlier_column],
        errors="coerce"
    ).dropna()


    if not outlier_series.empty:

        q1 = outlier_series.quantile(
            0.25
        )

        q3 = outlier_series.quantile(
            0.75
        )

        iqr = q3 - q1


        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )


        outliers = outlier_series[
            (
                outlier_series
                < lower_bound
            )
            |
            (
                outlier_series
                > upper_bound
            )
        ]


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Q1",
                f"{q1:,.2f}"
            )


        with col2:

            st.metric(
                "Q3",
                f"{q3:,.2f}"
            )


        with col3:

            st.metric(
                "Outliers",
                f"{len(outliers):,}"
            )


        st.write(
            f"Lower Bound: **{lower_bound:,.2f}**"
        )

        st.write(
            f"Upper Bound: **{upper_bound:,.2f}**"
        )


        if len(outliers) > 0:

            st.warning(
                f"⚠️ {len(outliers):,} "
                f"outlier(s) detected."
            )

        else:

            st.success(
                "✅ No outliers detected."
            )

else:

    st.info(
        "No numerical columns available "
        "for outlier analysis."
    )


# ============================================================
# AUTOMATIC EDA INSIGHTS
# ============================================================

st.divider()

st.header("💡 Quick EDA Insights")


insights = []


# ------------------------------------------------------------
# DATASET SIZE
# ------------------------------------------------------------

insights.append(
    f"The dataset contains "
    f"{len(analysis_df):,} rows and "
    f"{len(analysis_df.columns):,} columns."
)


# ------------------------------------------------------------
# MISSING VALUES
# ------------------------------------------------------------

total_missing = int(
    analysis_df.isnull()
    .sum()
    .sum()
)


if total_missing == 0:

    insights.append(
        "There are no missing values "
        "in the dataset."
    )

else:

    insights.append(
        f"The dataset contains "
        f"{total_missing:,} missing values."
    )


# ------------------------------------------------------------
# DUPLICATES
# ------------------------------------------------------------

total_duplicates = int(
    analysis_df.duplicated()
    .sum()
)


if total_duplicates == 0:

    insights.append(
        "No duplicate rows were detected."
    )

else:

    insights.append(
        f"{total_duplicates:,} "
        "duplicate rows were detected."
    )


# ------------------------------------------------------------
# NUMERICAL COLUMNS
# ------------------------------------------------------------

insights.append(
    f"The dataset contains "
    f"{len(numeric_columns)} numerical "
    f"column(s) and "
    f"{len(categorical_columns)} "
    "categorical column(s)."
)


# ------------------------------------------------------------
# DISPLAY INSIGHTS
# ------------------------------------------------------------

for insight in insights:

    st.info(
        f"💡 {insight}"
    )


# ============================================================
# NAVIGATION
# ============================================================

st.divider()

st.header("🚀 Continue")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# PREVIOUS PAGE
# ------------------------------------------------------------

with col1:

    if st.button(
        "⬅️ Previous: Cleaning",
        use_container_width=True,
        key="eda_previous_cleaning"
    ):

        st.switch_page(
            "pages/02_Cleaning.py"
        )


# ------------------------------------------------------------
# NEXT PAGE
# ------------------------------------------------------------

with col2:

    if st.button(
        "Next: Visualization ➡️",
        type="primary",
        use_container_width=True,
        key="eda_next_visualization"
    ):

        st.switch_page(
            "pages/04_Visualization.py"
        )