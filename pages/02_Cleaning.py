import streamlit as st
import pandas as pd
import numpy as np


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Cleaning",
    page_icon="🧹",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "dataset" not in st.session_state:
    st.session_state["dataset"] = None

if "cleaned_data" not in st.session_state:
    st.session_state["cleaned_data"] = None

if "cleaning_summary" not in st.session_state:
    st.session_state["cleaning_summary"] = {}


# ============================================================
# TITLE
# ============================================================

st.title("🧹 Data Cleaning")

st.write(
    "Clean your dataset by handling missing values, "
    "duplicates, incorrect data types, outliers, and "
    "unnecessary columns."
)


# ============================================================
# CHECK DATASET
# ============================================================

df = st.session_state.get(
    "dataset"
)


if df is None:

    st.warning(
        "⚠️ Please upload a dataset first."
    )

    if st.button(
        "📤 Go to Upload Dataset",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/01_Upload.py"
        )

    st.stop()


# ============================================================
# USE CLEANED DATA IF AVAILABLE
# ============================================================

if st.session_state.get("cleaned_data") is not None:

    working_df = st.session_state[
        "cleaned_data"
    ].copy()

else:

    working_df = df.copy()


# ============================================================
# DATASET STATUS
# ============================================================

st.success(
    f"✅ Dataset loaded: "
    f"{st.session_state.get('file_name', 'Dataset')}"
)


# ============================================================
# DATASET METRICS
# ============================================================

st.subheader(
    "📊 Current Dataset Status"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Rows",
        f"{len(working_df):,}"
    )


with col2:

    st.metric(
        "Columns",
        f"{len(working_df.columns):,}"
    )


with col3:

    st.metric(
        "Missing Values",
        f"{int(working_df.isnull().sum().sum()):,}"
    )


with col4:

    st.metric(
        "Duplicate Rows",
        f"{int(working_df.duplicated().sum()):,}"
    )


# ============================================================
# CLEANING OPTIONS
# ============================================================

st.divider()

st.subheader(
    "🧹 Cleaning Options"
)


# ============================================================
# 1. REMOVE DUPLICATES
# ============================================================

with st.expander(
    "1️⃣ Remove Duplicate Rows",
    expanded=True
):

    duplicate_count = int(
        working_df.duplicated().sum()
    )

    if duplicate_count > 0:

        st.warning(
            f"{duplicate_count:,} duplicate rows detected."
        )

        remove_duplicates = st.checkbox(
            "Remove duplicate rows",
            key="remove_duplicates"
        )

    else:

        st.success(
            "✅ No duplicate rows detected."
        )

        remove_duplicates = False


# ============================================================
# 2. MISSING VALUES
# ============================================================

with st.expander(
    "2️⃣ Handle Missing Values",
    expanded=True
):

    missing_total = int(
        working_df.isnull()
        .sum()
        .sum()
    )

    if missing_total == 0:

        st.success(
            "✅ No missing values detected."
        )

        missing_action = "None"

    else:

        st.warning(
            f"{missing_total:,} missing values detected."
        )

        missing_action = st.selectbox(
            "Choose missing-value treatment",
            [
                "Do Nothing",
                "Drop Rows",
                "Fill Numerical with Mean",
                "Fill Numerical with Median",
                "Fill Numerical with 0",
                "Fill Categorical with Mode",
                "Fill All with 0"
            ],
            key="missing_action"
        )


# ============================================================
# 3. DROP COLUMNS
# ============================================================

with st.expander(
    "3️⃣ Remove Unnecessary Columns"
):

    columns_to_drop = st.multiselect(
        "Select columns to remove",
        working_df.columns.tolist(),
        key="columns_to_drop"
    )

    if columns_to_drop:

        st.warning(
            f"{len(columns_to_drop)} column(s) "
            "will be removed."
        )


# ============================================================
# 4. DATA TYPE CONVERSION
# ============================================================

with st.expander(
    "4️⃣ Convert Data Types"
):

    selected_column = st.selectbox(
        "Select column",
        working_df.columns.tolist(),
        key="datatype_column"
    )

    selected_type = st.selectbox(
        "Convert to",
        [
            "No Conversion",
            "Integer",
            "Float",
            "String",
            "Category",
            "Date"
        ],
        key="datatype_type"
    )


# ============================================================
# 5. REMOVE CONSTANT COLUMNS
# ============================================================

with st.expander(
    "5️⃣ Detect Constant Columns"
):

    constant_columns = []

    for column in working_df.columns:

        if working_df[column].nunique(
            dropna=False
        ) <= 1:

            constant_columns.append(
                column
            )

    if constant_columns:

        st.warning(
            "Constant columns detected:"
        )

        st.write(
            constant_columns
        )

        remove_constant = st.checkbox(
            "Remove constant columns",
            key="remove_constant"
        )

    else:

        st.success(
            "✅ No constant columns detected."
        )

        remove_constant = False


# ============================================================
# 6. INFINITE VALUES
# ============================================================

with st.expander(
    "6️⃣ Handle Infinite Values"
):

    numeric_columns = working_df.select_dtypes(
        include=np.number
    ).columns.tolist()

    infinite_count = 0

    if numeric_columns:

        infinite_count = int(
            np.isinf(
                working_df[
                    numeric_columns
                ]
            ).sum().sum()
        )

    if infinite_count > 0:

        st.warning(
            f"{infinite_count:,} infinite values detected."
        )

        replace_inf = st.checkbox(
            "Replace infinite values with NaN",
            key="replace_inf"
        )

    else:

        st.success(
            "✅ No infinite values detected."
        )

        replace_inf = False


# ============================================================
# 7. OUTLIER DETECTION
# ============================================================

with st.expander(
    "7️⃣ Outlier Detection"
):

    numeric_columns = working_df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if not numeric_columns:

        st.info(
            "No numerical columns available "
            "for outlier detection."
        )

        outlier_action = "None"

    else:

        outlier_column = st.selectbox(
            "Select numerical column",
            numeric_columns,
            key="outlier_column"
        )

        outlier_action = st.selectbox(
            "Outlier treatment",
            [
                "None",
                "Remove Outliers",
                "Cap Outliers"
            ],
            key="outlier_action"
        )


# ============================================================
# 8. COLUMN NAME CLEANING
# ============================================================

with st.expander(
    "8️⃣ Clean Column Names"
):

    clean_column_names = st.checkbox(
        "Remove spaces and standardize column names",
        value=True,
        key="clean_column_names"
    )


# ============================================================
# APPLY CLEANING
# ============================================================

st.divider()

st.subheader(
    "⚙️ Apply Cleaning"
)


if st.button(
    "🚀 Apply Selected Cleaning",
    type="primary",
    use_container_width=True
):

    cleaned_df = working_df.copy()

    original_rows = len(cleaned_df)

    original_columns = len(
        cleaned_df.columns
    )

    changes = []


    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    if remove_duplicates:

        before = len(cleaned_df)

        cleaned_df = (
            cleaned_df
            .drop_duplicates()
            .reset_index(drop=True)
        )

        removed = before - len(cleaned_df)

        changes.append(
            f"Removed {removed:,} duplicate rows"
        )


    # --------------------------------------------------------
    # INFINITE VALUES
    # --------------------------------------------------------

    if replace_inf:

        numeric_cols = (
            cleaned_df
            .select_dtypes(
                include=np.number
            )
            .columns
        )

        if len(numeric_cols) > 0:

            cleaned_df[numeric_cols] = (
                cleaned_df[numeric_cols]
                .replace(
                    [np.inf, -np.inf],
                    np.nan
                )
            )

            changes.append(
                "Replaced infinite values with NaN"
            )


    # --------------------------------------------------------
    # MISSING VALUES
    # --------------------------------------------------------

    if missing_action == "Drop Rows":

        before = len(cleaned_df)

        cleaned_df = (
            cleaned_df
            .dropna()
            .reset_index(drop=True)
        )

        removed = before - len(cleaned_df)

        changes.append(
            f"Dropped {removed:,} rows "
            "containing missing values"
        )


    elif missing_action == "Fill Numerical with Mean":

        numeric_cols = (
            cleaned_df
            .select_dtypes(
                include=np.number
            )
            .columns
        )

        for column in numeric_cols:

            if cleaned_df[column].isnull().any():

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(
                        cleaned_df[column].mean()
                    )
                )

        changes.append(
            "Filled numerical missing values with mean"
        )


    elif missing_action == "Fill Numerical with Median":

        numeric_cols = (
            cleaned_df
            .select_dtypes(
                include=np.number
            )
            .columns
        )

        for column in numeric_cols:

            if cleaned_df[column].isnull().any():

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(
                        cleaned_df[column].median()
                    )
                )

        changes.append(
            "Filled numerical missing values with median"
        )


    elif missing_action == "Fill Numerical with 0":

        numeric_cols = (
            cleaned_df
            .select_dtypes(
                include=np.number
            )
            .columns
        )

        cleaned_df[numeric_cols] = (
            cleaned_df[numeric_cols]
            .fillna(0)
        )

        changes.append(
            "Filled numerical missing values with 0"
        )


    elif missing_action == "Fill Categorical with Mode":

        categorical_cols = (
            cleaned_df
            .select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            )
            .columns
        )

        for column in categorical_cols:

            if cleaned_df[column].isnull().any():

                mode = (
                    cleaned_df[column]
                    .mode()
                )

                if not mode.empty:

                    cleaned_df[column] = (
                        cleaned_df[column]
                        .fillna(mode.iloc[0])
                    )

        changes.append(
            "Filled categorical missing values with mode"
        )


    elif missing_action == "Fill All with 0":

        cleaned_df = (
            cleaned_df
            .fillna(0)
        )

        changes.append(
            "Filled all missing values with 0"
        )


    # --------------------------------------------------------
    # DROP COLUMNS
    # --------------------------------------------------------

    if columns_to_drop:

        cleaned_df = (
            cleaned_df
            .drop(
                columns=columns_to_drop,
                errors="ignore"
            )
        )

        changes.append(
            f"Removed {len(columns_to_drop)} column(s)"
        )


    # --------------------------------------------------------
    # REMOVE CONSTANT COLUMNS
    # --------------------------------------------------------

    if remove_constant:

        constant_to_remove = []

        for column in cleaned_df.columns:

            if cleaned_df[column].nunique(
                dropna=False
            ) <= 1:

                constant_to_remove.append(
                    column
                )

        if constant_to_remove:

            cleaned_df = (
                cleaned_df
                .drop(
                    columns=constant_to_remove
                )
            )

            changes.append(
                f"Removed {len(constant_to_remove)} "
                "constant column(s)"
            )


    # --------------------------------------------------------
    # DATA TYPE CONVERSION
    # --------------------------------------------------------

    if (
        selected_column in cleaned_df.columns
        and selected_type != "No Conversion"
    ):

        try:

            if selected_type == "Integer":

                cleaned_df[selected_column] = pd.to_numeric(
                    cleaned_df[selected_column],
                    errors="coerce"
                ).astype("Int64")


            elif selected_type == "Float":

                cleaned_df[selected_column] = pd.to_numeric(
                    cleaned_df[selected_column],
                    errors="coerce"
                )


            elif selected_type == "String":

                cleaned_df[selected_column] = (
                    cleaned_df[selected_column]
                    .astype(str)
                )


            elif selected_type == "Category":

                cleaned_df[selected_column] = (
                    cleaned_df[selected_column]
                    .astype("category")
                )


            elif selected_type == "Date":

                cleaned_df[selected_column] = (
                    pd.to_datetime(
                        cleaned_df[selected_column],
                        errors="coerce"
                    )
                )


            changes.append(
                f"Converted {selected_column} "
                f"to {selected_type}"
            )

        except Exception as e:

            st.warning(
                f"Could not convert "
                f"{selected_column}: {e}"
            )


    # --------------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------------

    if clean_column_names:

        new_columns = []

        for column in cleaned_df.columns:

            new_column = (
                str(column)
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            new_columns.append(
                new_column
            )

        cleaned_df.columns = new_columns

        changes.append(
            "Standardized column names"
        )


    # --------------------------------------------------------
    # OUTLIERS
    # --------------------------------------------------------

    if (
        outlier_action != "None"
        and outlier_column in cleaned_df.columns
    ):

        series = pd.to_numeric(
            cleaned_df[outlier_column],
            errors="coerce"
        )

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr


        if outlier_action == "Remove Outliers":

            mask = (
                (series >= lower)
                & (series <= upper)
            )

            cleaned_df = (
                cleaned_df[
                    mask.fillna(False)
                ]
                .reset_index(drop=True)
            )

            changes.append(
                f"Removed outliers from "
                f"{outlier_column}"
            )


        elif outlier_action == "Cap Outliers":

            cleaned_df[
                outlier_column
            ] = series.clip(
                lower=lower,
                upper=upper
            )

            changes.append(
                f"Capped outliers in "
                f"{outlier_column}"
            )


    # --------------------------------------------------------
    # SAVE CLEANED DATA
    # --------------------------------------------------------

    st.session_state[
        "cleaned_data"
    ] = cleaned_df


    # --------------------------------------------------------
    # CLEANING SUMMARY
    # --------------------------------------------------------

    st.session_state[
        "cleaning_summary"
    ] = {

        "original_rows":
            original_rows,

        "final_rows":
            len(cleaned_df),

        "original_columns":
            original_columns,

        "final_columns":
            len(cleaned_df.columns),

        "changes":
            changes
    }


    st.success(
        "✅ Cleaning completed successfully!"
    )

    st.rerun()


# ============================================================
# CLEANING RESULTS
# ============================================================

if st.session_state.get(
    "cleaned_data"
) is not None:

    cleaned_df = st.session_state[
        "cleaned_data"
    ]


    st.divider()

    st.subheader(
        "✅ Cleaned Dataset"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Rows",
            f"{len(cleaned_df):,}",
            f"{len(cleaned_df) - len(df):,}"
        )


    with col2:

        st.metric(
            "Columns",
            f"{len(cleaned_df.columns):,}",
            f"{len(cleaned_df.columns) - len(df.columns):,}"
        )


    with col3:

        st.metric(
            "Missing Values",
            f"{int(cleaned_df.isnull().sum().sum()):,}"
        )


    with col4:

        st.metric(
            "Duplicates",
            f"{int(cleaned_df.duplicated().sum()):,}"
        )


    st.dataframe(
        cleaned_df.head(10),
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # CHANGES
    # --------------------------------------------------------

    summary = st.session_state.get(
        "cleaning_summary",
        {}
    )

    changes = summary.get(
        "changes",
        []
    )


    if changes:

        st.subheader(
            "📝 Cleaning Summary"
        )

        for change in changes:

            st.write(
                f"✅ {change}"
            )


    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    csv = cleaned_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        "⬇️ Download Cleaned Dataset",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )
# ============================================================
# PAGE NAVIGATION
# ============================================================

st.divider()

st.subheader("🚀 Continue")

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# PREVIOUS PAGE
# ------------------------------------------------------------

with col1:

    if st.button(
        "⬅️ Previous: Upload",
        use_container_width=True,
        key="cleaning_previous_upload"
    ):

        st.switch_page(
            "pages/01_Upload.py"
        )


# ------------------------------------------------------------
# NEXT PAGE
# ------------------------------------------------------------

with col2:

    if st.button(
        "Next: EDA ➡️",
        type="primary",
        use_container_width=True,
        key="cleaning_next_eda"
    ):

        st.switch_page(
            "pages/03_EDA.py"
        )