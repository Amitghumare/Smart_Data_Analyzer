import streamlit as st

from src.session.state import initialize_session_state


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart Data Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# INITIALIZE SESSION
# ============================================================

initialize_session_state()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #666;
        margin-bottom: 40px;
    }

    .feature-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
        min-height: 150px;
    }

    .feature-title {
        font-size: 22px;
        font-weight: 600;
    }

    .feature-description {
        color: #666;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📊 Smart Data Analyzer")

    st.divider()

    st.subheader("Dataset Status")

    if st.session_state["dataset"] is not None:

        df = st.session_state["dataset"]

        st.success(
            "✅ Dataset Loaded"
        )

        st.write(
            f"**File:** "
            f"{st.session_state.get('file_name', 'Unknown')}"
        )

        st.write(
            f"**Rows:** {df.shape[0]:,}"
        )

        st.write(
            f"**Columns:** {df.shape[1]:,}"
        )

        if (
            st.session_state.get(
                "cleaned_data"
            )
            is not None
        ):

            st.success(
                "🧹 Cleaned Dataset Available"
            )

    else:

        st.warning(
            "⚠️ No Dataset Loaded"
        )


    st.divider()

    st.caption(
        "Upload → Clean → Analyze → Visualize → Report"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📊 Smart Data Analyzer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Upload any CSV, TSV or Excel dataset and
    automatically clean, analyze, visualize,
    understand and report your data.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CURRENT DATASET
# ============================================================

if st.session_state["dataset"] is not None:

    df = st.session_state["dataset"]

    st.success(
        "✅ Current dataset: "
        f"**{st.session_state.get('file_name', 'Dataset')}**"
    )


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

        missing = int(
            df.isnull()
            .sum()
            .sum()
        )

        st.metric(
            "Missing Values",
            f"{missing:,}"
        )


    with col4:

        duplicates = int(
            df.duplicated()
            .sum()
        )

        st.metric(
            "Duplicates",
            f"{duplicates:,}"
        )


else:

    st.info(
        "👋 Welcome! Upload a dataset to start."
    )


# ============================================================
# FEATURES
# ============================================================

st.divider()

st.header(
    "🚀 What can you do?"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        📤 Upload
        </div>

        <p class="feature-description">
        Upload CSV, TSV or Excel datasets
        and inspect their structure.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        🧹 Clean
        </div>

        <p class="feature-description">
        Handle missing values, duplicates,
        data types and quality issues.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        🔍 Explore
        </div>

        <p class="feature-description">
        Perform automated exploratory
        data analysis.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        📊 Visualize
        </div>

        <p class="feature-description">
        Create charts and explore
        relationships between variables.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        🧠 Insights
        </div>

        <p class="feature-description">
        Automatically discover patterns,
        trends and correlations.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        📄 Reports
        </div>

        <p class="feature-description">
        Generate and download a
        complete analysis report.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GET STARTED
# ============================================================

st.divider()

st.header(
    "🎯 Get Started"
)


if st.session_state["dataset"] is None:

    if st.button(
        "📤 Upload Your Dataset",
        type="primary",
        use_container_width=True,
        key="home_upload_dataset"
    ):

        st.switch_page(
            "pages/01_Upload.py"
        )


else:

    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🧹 Continue Analysis",
            type="primary",
            use_container_width=True,
            key="home_continue_analysis"
        ):

            st.switch_page(
                "pages/02_Cleaning.py"
            )


    with col2:

        if st.button(
            "📄 Generate Report",
            use_container_width=True,
            key="home_generate_report"
        ):

            st.switch_page(
                "pages/06_Reports.py"
            )


# ============================================================
# WORKFLOW
# ============================================================

st.divider()

st.header(
    "🔄 Analysis Workflow"
)


steps = [

    (
        "1",
        "📤 Upload",
        "Upload your dataset"
    ),

    (
        "2",
        "🧹 Clean",
        "Fix data-quality issues"
    ),

    (
        "3",
        "🔍 EDA",
        "Explore the dataset"
    ),

    (
        "4",
        "📊 Visualize",
        "Create visualizations"
    ),

    (
        "5",
        "🧠 Insights",
        "Discover patterns"
    ),

    (
        "6",
        "📄 Reports",
        "Download your report"
    )

]


for number, title, description in steps:

    col1, col2, col3 = st.columns(
        [1, 3, 6]
    )

    with col1:

        st.markdown(
            f"### {number}"
        )

    with col2:

        st.markdown(
            f"**{title}**"
        )

    with col3:

        st.write(
            description
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Smart Data Analyzer • Automated Data Analysis Platform"
)