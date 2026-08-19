import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
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

st.title("📄 Data Analysis Report")

st.markdown(
    """
    Generate a complete report containing dataset information,
    data quality, statistical analysis, insights, and
    recommendations.
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

    data_source = "Cleaned Dataset"

    st.success(
        "✅ Report is being generated from the cleaned dataset."
    )


# ------------------------------------------------------------
# USE ORIGINAL DATA
# ------------------------------------------------------------

elif (
    dataset is not None
    and isinstance(dataset, pd.DataFrame)
    and not dataset.empty
):

    df = dataset.copy()

    data_source = "Original Dataset"

    st.info(
        "ℹ️ Report is being generated from the original dataset."
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
        key="reports_go_upload"
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
# BASIC INFORMATION
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


rows = df.shape[0]

columns = df.shape[1]

missing_values = int(
    df.isnull()
    .sum()
    .sum()
)

duplicate_rows = int(
    df.duplicated()
    .sum()
)


missing_percentage = (
    missing_values
    /
    (rows * columns)
    *
    100
    if rows > 0 and columns > 0
    else 0
)


# ============================================================
# REPORT INFORMATION
# ============================================================

report_date = datetime.now().strftime(
    "%d %B %Y, %I:%M %p"
)

file_name = (
    st.session_state.get("file_name")
    or "Dataset"
)


# ============================================================
# REPORT SUMMARY
# ============================================================

st.divider()

st.header("📊 Report Summary")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Rows",
        f"{rows:,}"
    )


with col2:

    st.metric(
        "Columns",
        f"{columns:,}"
    )


with col3:

    st.metric(
        "Missing Values",
        f"{missing_values:,}"
    )


with col4:

    st.metric(
        "Duplicate Rows",
        f"{duplicate_rows:,}"
    )


# ============================================================
# DATASET DETAILS
# ============================================================

st.divider()

st.header("📁 Dataset Details")


dataset_details = pd.DataFrame({

    "Property": [
        "File Name",
        "Data Source",
        "Rows",
        "Columns",
        "Numerical Columns",
        "Categorical Columns",
        "Missing Values",
        "Missing Percentage",
        "Duplicate Rows",
        "Report Generated"
    ],

    "Value": [
        file_name,
        data_source,
        f"{rows:,}",
        f"{columns:,}",
        len(numeric_columns),
        len(categorical_columns),
        f"{missing_values:,}",
        f"{missing_percentage:.2f}%",
        f"{duplicate_rows:,}",
        report_date
    ]
})


st.dataframe(
    dataset_details,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DATA QUALITY
# ============================================================

st.divider()

st.header("🔎 Data Quality")


quality_data = []


for column in df.columns:

    missing = int(
        df[column]
        .isnull()
        .sum()
    )

    missing_pct = (
        missing
        /
        len(df)
        *
        100
        if len(df) > 0
        else 0
    )

    duplicates = int(
        df[column]
        .duplicated()
        .sum()
    )

    unique = int(
        df[column]
        .nunique(
            dropna=True
        )
    )


    quality_data.append({

        "Column":
            column,

        "Data Type":
            str(
                df[column].dtype
            ),

        "Missing Values":
            missing,

        "Missing %":
            round(
                missing_pct,
                2
            ),

        "Unique Values":
            unique,

        "Duplicate Values":
            duplicates

    })


quality_df = pd.DataFrame(
    quality_data
)


st.dataframe(
    quality_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# STATISTICAL SUMMARY
# ============================================================

st.divider()

st.header("📈 Statistical Summary")


if numeric_columns:

    statistics = (
        df[numeric_columns]
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

    statistics = pd.DataFrame()

    st.info(
        "No numerical columns available."
    )


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

st.divider()

st.header("🔗 Correlation Analysis")


correlation_pairs = []


if len(numeric_columns) >= 2:

    correlation_matrix = (
        df[numeric_columns]
        .corr()
    )


    for i in range(
        len(correlation_matrix.columns)
    ):

        for j in range(
            i + 1,
            len(correlation_matrix.columns)
        ):

            col1 = (
                correlation_matrix
                .columns[i]
            )

            col2 = (
                correlation_matrix
                .columns[j]
            )


            value = (
                correlation_matrix
                .iloc[i, j]
            )


            if not pd.isna(value):

                correlation_pairs.append({

                    "Column 1":
                        col1,

                    "Column 2":
                        col2,

                    "Correlation":
                        round(
                            value,
                            3
                        ),

                    "Absolute Correlation":
                        abs(value)

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


        display_correlation = (
            correlation_df
            .drop(
                columns=[
                    "Absolute Correlation"
                ]
            )
            .head(10)
        )


        st.dataframe(
            display_correlation,
            use_container_width=True,
            hide_index=True
        )


    else:

        correlation_df = pd.DataFrame()

        st.info(
            "No valid correlations found."
        )


else:

    correlation_df = pd.DataFrame()

    st.info(
        "At least two numerical columns "
        "are required."
    )


# ============================================================
# AUTOMATIC INSIGHTS
# ============================================================

st.divider()

st.header("💡 Key Insights")


insights = []


# ------------------------------------------------------------
# DATASET SIZE
# ------------------------------------------------------------

insights.append(
    f"The dataset contains **{rows:,} rows** "
    f"and **{columns:,} columns**."
)


# ------------------------------------------------------------
# COLUMN TYPES
# ------------------------------------------------------------

insights.append(
    f"There are **{len(numeric_columns)} numerical** "
    f"and **{len(categorical_columns)} categorical** "
    f"columns."
)


# ------------------------------------------------------------
# MISSING VALUES
# ------------------------------------------------------------

if missing_values == 0:

    insights.append(
        "✅ No missing values were detected."
    )

else:

    insights.append(
        f"⚠️ The dataset contains **{missing_values:,} "
        f"missing values ({missing_percentage:.2f}%)**."
    )


# ------------------------------------------------------------
# DUPLICATES
# ------------------------------------------------------------

if duplicate_rows == 0:

    insights.append(
        "✅ No duplicate rows were detected."
    )

else:

    insights.append(
        f"⚠️ **{duplicate_rows:,} duplicate rows** "
        "were detected."
    )


# ------------------------------------------------------------
# STRONGEST CORRELATION
# ------------------------------------------------------------

if correlation_pairs:

    strongest = (
        correlation_df
        .iloc[0]
    )


    correlation_value = (
        strongest["Correlation"]
    )


    if abs(correlation_value) >= 0.7:

        strength = "strong"

    elif abs(correlation_value) >= 0.4:

        strength = "moderate"

    else:

        strength = "weak"


    direction = (
        "positive"
        if correlation_value > 0
        else "negative"
    )


    insights.append(
        f"🔗 The strongest relationship is between "
        f"**{strongest['Column 1']}** and "
        f"**{strongest['Column 2']}**, with a "
        f"{strength} {direction} correlation of "
        f"**{correlation_value:.3f}**."
    )


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------

for insight in insights:

    st.info(
        insight
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.divider()

st.header("🎯 Recommendations")


recommendations = []


if missing_values > 0:

    recommendations.append(
        "Review missing values and decide whether "
        "to impute, remove, or retain them."
    )

else:

    recommendations.append(
        "No missing-value treatment is required."
    )


if duplicate_rows > 0:

    recommendations.append(
        "Review duplicate rows and remove them "
        "if they represent duplicate records."
    )

else:

    recommendations.append(
        "No duplicate-row treatment is required."
    )


if numeric_columns:

    recommendations.append(
        "Review numerical distributions and "
        "outliers before applying machine learning."
    )


if categorical_columns:

    recommendations.append(
        "Review categorical variables for rare "
        "categories and inconsistent labels."
    )


if correlation_pairs:

    recommendations.append(
        "Investigate highly correlated variables "
        "for potential relationships or multicollinearity."
    )


for i, recommendation in enumerate(
    recommendations,
    start=1
):

    st.write(
        f"**{i}.** {recommendation}"
    )


# ============================================================
# REPORT PREVIEW
# ============================================================

st.divider()

st.header("📄 Report Preview")


report_html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>Smart Data Analyzer Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    color: #222;
}}

h1 {{
    color: #1f4e79;
}}

h2 {{
    color: #2f75b5;
    border-bottom: 1px solid #ddd;
    padding-bottom: 5px;
}}

.summary {{
    background: #f4f6f8;
    padding: 15px;
    border-radius: 8px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}}

th {{
    background: #f2f2f2;
}}

.insight {{
    padding: 10px;
    margin: 5px 0;
    background: #eef5ff;
    border-radius: 5px;
}}

.recommendation {{
    padding: 10px;
    margin: 5px 0;
    background: #f5f5f5;
    border-radius: 5px;
}}

</style>

</head>


<body>


<h1>📊 Smart Data Analyzer Report</h1>


<p>
<strong>Dataset:</strong> {file_name}
</p>

<p>
<strong>Data Source:</strong> {data_source}
</p>

<p>
<strong>Generated:</strong> {report_date}
</p>


<h2>Dataset Summary</h2>


<div class="summary">

<p>
<strong>Rows:</strong> {rows:,}
</p>

<p>
<strong>Columns:</strong> {columns:,}
</p>

<p>
<strong>Numerical Columns:</strong>
{len(numeric_columns)}
</p>

<p>
<strong>Categorical Columns:</strong>
{len(categorical_columns)}
</p>

<p>
<strong>Missing Values:</strong>
{missing_values:,}
</p>

<p>
<strong>Duplicate Rows:</strong>
{duplicate_rows:,}
</p>

</div>


<h2>Column Information</h2>

{quality_df.to_html(
    index=False,
    border=0
)}


<h2>Statistical Summary</h2>

{
    statistics.to_html(
        index=False,
        border=0
    )
    if not statistics.empty
    else "<p>No numerical columns available.</p>"
}


<h2>Key Insights</h2>

{
    "".join(
        f'<div class="insight">{insight.replace("**", "")}</div>'
        for insight in insights
    )
}


<h2>Recommendations</h2>

{
    "".join(
        f'<div class="recommendation">{recommendation}</div>'
        for recommendation in recommendations
    )
}


</body>

</html>
"""


st.components.v1.html(
    report_html,
    height=600,
    scrolling=True
)


# ============================================================
# DOWNLOAD REPORT
# ============================================================

st.divider()

st.header("⬇️ Download Report")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# HTML REPORT
# ------------------------------------------------------------

with col1:

    st.download_button(
        label="📄 Download HTML Report",
        data=report_html,
        file_name="smart_data_analysis_report.html",
        mime="text/html",
        use_container_width=True,
        key="download_html_report"
    )


# ------------------------------------------------------------
# CSV SUMMARY
# ------------------------------------------------------------

with col2:

    csv_data = quality_df.to_csv(
        index=False
    )


    st.download_button(
        label="📊 Download Data Quality CSV",
        data=csv_data,
        file_name="data_quality_report.csv",
        mime="text/csv",
        use_container_width=True,
        key="download_quality_csv"
    )


# ============================================================
# NAVIGATION
# ============================================================

st.divider()

st.header("🚀 Navigation")


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# PREVIOUS
# ------------------------------------------------------------

with col1:

    if st.button(
        "⬅️ Previous: Insights",
        use_container_width=True,
        key="reports_previous_insights"
    ):

        st.switch_page(
            "pages/05_Insights.py"
        )


# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------

with col2:

    if st.button(
        "🏠 Back to Upload",
        type="primary",
        use_container_width=True,
        key="reports_back_upload"
    ):

        st.switch_page(
            "pages/01_Upload.py"
        )