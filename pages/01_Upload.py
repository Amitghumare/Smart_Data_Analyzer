import streamlit as st
import pandas as pd

from src.session.state import initialize_session_state
from src.data_loader.loader import load_dataset
from src.utils.validator import validate_dataset


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📤",
    layout="wide"
)


# ============================================================
# INITIALIZE SESSION
# ============================================================

initialize_session_state()


# ============================================================
# TITLE
# ============================================================

st.title("📤 Upload Dataset")

st.markdown(
    """
    Upload a CSV, TSV or Excel dataset to begin your
    automated data analysis.
    """
)


# ============================================================
# SIDEBAR DATASET STATUS
# ============================================================

with st.sidebar:

    st.header("📊 Dataset Status")

    if st.session_state["dataset"] is not None:

        current_df = st.session_state["dataset"]

        st.success("✅ Dataset Loaded")

        st.write(
            f"**File:** "
            f"{st.session_state.get('file_name', 'Unknown')}"
        )

        st.write(
            f"**Rows:** {current_df.shape[0]:,}"
        )

        st.write(
            f"**Columns:** {current_df.shape[1]:,}"
        )

        if (
            st.session_state.get(
                "cleaned_data"
            )
            is not None
        ):

            st.success(
                "🧹 Cleaned data available"
            )

    else:

        st.warning(
            "⚠️ No dataset uploaded"
        )


# ============================================================
# FILE UPLOADER
# ============================================================

uploaded_file = st.file_uploader(
    "Choose your dataset",
    type=[
        "csv",
        "tsv",
        "xlsx",
        "xls"
    ],
    help=(
        "Supported formats: CSV, TSV, "
        "XLSX and XLS"
    ),
    key="dataset_uploader"
)


# ============================================================
# LOAD DATASET
# ============================================================

if uploaded_file is not None:

    # --------------------------------------------------------
    # CHECK IF THIS IS A NEW FILE
    # --------------------------------------------------------

    previous_file = st.session_state.get(
        "file_name"
    )

    is_new_file = (
        previous_file != uploaded_file.name
    )


    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    try:

        with st.spinner(
            "📥 Loading dataset..."
        ):

            df = load_dataset(
                uploaded_file
            )


        # ----------------------------------------------------
        # CLEAN COLUMN NAMES
        # ----------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )


        # ----------------------------------------------------
        # VALIDATE
        # ----------------------------------------------------

        valid, errors, warnings = (
            validate_dataset(df)
        )


        # ----------------------------------------------------
        # VALIDATION ERRORS
        # ----------------------------------------------------

        if not valid:

            st.error(
                "❌ Dataset validation failed."
            )

            for error in errors:

                st.error(
                    f"• {error}"
                )

            st.stop()


        # ----------------------------------------------------
        # WARNINGS
        # ----------------------------------------------------

        if warnings:

            st.warning(
                "⚠️ Dataset loaded with warnings."
            )

            with st.expander(
                "🔎 View Dataset Warnings"
            ):

                for warning in warnings:

                    st.write(
                        f"• {warning}"
                    )


        # ----------------------------------------------------
        # SAVE DATASET
        # ----------------------------------------------------

        if is_new_file:

            st.session_state["dataset"] = (
                df.copy()
            )

            st.session_state[
                "cleaned_data"
            ] = None

            st.session_state[
                "cleaning_applied"
            ] = False

            st.session_state[
                "visualizations"
            ] = []

            st.session_state[
                "insights"
            ] = []

            st.session_state[
                "report_generated"
            ] = False

            st.session_state[
                "dataset_loaded"
            ] = True

            st.session_state[
                "file_name"
            ] = uploaded_file.name


        else:

            # Keep existing dataset if
            # Streamlit reruns the page.

            df = st.session_state[
                "dataset"
            ]


        st.success(
            f"✅ Successfully loaded: "
            f"**{uploaded_file.name}**"
        )


    except Exception as e:

        st.error(
            f"❌ Error loading dataset: {str(e)}"
        )

        st.stop()


# ============================================================
# DISPLAY CURRENT DATASET
# ============================================================

if st.session_state["dataset"] is not None:

    df = st.session_state["dataset"]


    # ========================================================
    # DATASET METRICS
    # ========================================================

    st.divider()

    st.subheader("📊 Dataset Overview")


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

        missing_values = int(
            df.isnull()
            .sum()
            .sum()
        )

        st.metric(
            "Missing Values",
            f"{missing_values:,}"
        )


    with col4:

        duplicate_rows = int(
            df.duplicated()
            .sum()
        )

        st.metric(
            "Duplicate Rows",
            f"{duplicate_rows:,}"
        )


    # ========================================================
    # DATA PREVIEW
    # ========================================================

    st.divider()

    st.subheader("👀 Data Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # DATA TYPES
    # ========================================================

    st.divider()

    st.subheader("🔤 Data Types")

    dtype_df = pd.DataFrame({

        "Column":
            df.columns,

        "Data Type":
            [
                str(dtype)
                for dtype in df.dtypes
            ],

        "Missing Values":
            [
                int(
                    df[column]
                    .isnull()
                    .sum()
                )

                for column in df.columns
            ],

        "Unique Values":
            [
                int(
                    df[column]
                    .nunique(
                        dropna=True
                    )
                )

                for column in df.columns
            ]

    })


    st.dataframe(
        dtype_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # NEXT PAGE
    # ========================================================

    st.divider()

    st.subheader(
        "🚀 Continue Analysis"
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # RE-UPLOAD
    # --------------------------------------------------------

    with col1:

        if st.button(
            "🔄 Upload Another Dataset",
            use_container_width=True,
            key="upload_another_dataset"
        ):

            st.session_state[
                "dataset"
            ] = None

            st.session_state[
                "cleaned_data"
            ] = None

            st.session_state[
                "file_name"
            ] = None

            st.session_state[
                "dataset_loaded"
            ] = False

            st.session_state[
                "cleaning_applied"
            ] = False

            st.rerun()


    # --------------------------------------------------------
    # NEXT
    # --------------------------------------------------------

    with col2:

        if st.button(
            "🧹 Next: Data Cleaning ➡️",
            type="primary",
            use_container_width=True,
            key="upload_next_cleaning"
        ):

            st.switch_page(
                "pages/02_Cleaning.py"
            )


else:

    # ========================================================
    # NO DATASET MESSAGE
    # ========================================================

    st.info(
        "👆 Upload a CSV, TSV or Excel file above "
        "to start."
    )