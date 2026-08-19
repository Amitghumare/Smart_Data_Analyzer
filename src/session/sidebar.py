import streamlit as st

from src.session.state import initialize_session


def show_dataset_status():

    initialize_session()

    with st.sidebar:

        st.header("📁 Dataset")

        if st.session_state.original_df is not None:

            st.success("🟢 Dataset Loaded")

            st.write(
                f"**File:** "
                f"{st.session_state.file_name}"
            )

            st.write(
                f"**Rows:** "
                f"{st.session_state.cleaned_df.shape[0]}"
            )

            st.write(
                f"**Columns:** "
                f"{st.session_state.cleaned_df.shape[1]}"
            )

            st.divider()

            st.write("**Dataset Status**")

            original_rows = (
                st.session_state.original_df.shape[0]
            )

            cleaned_rows = (
                st.session_state.cleaned_df.shape[0]
            )

            if original_rows != cleaned_rows:

                st.info(
                    f"🧹 {original_rows - cleaned_rows} "
                    f"rows removed during cleaning."
                )

            else:

                st.info(
                    "No rows removed yet."
                )

        else:

            st.warning(
                "⚠️ No dataset loaded"
            )

            st.write(
                "Go to the Home page and "
                "upload a dataset."
            )