import io
import pandas as pd


def load_dataset(uploaded_file):
    """
    Load CSV, TSV, XLSX or XLS file uploaded through Streamlit.

    Returns:
        pandas.DataFrame
    """

    if uploaded_file is None:

        raise ValueError(
            "No file was uploaded."
        )

    file_name = uploaded_file.name.lower()

    try:

        # ====================================================
        # CSV
        # ====================================================

        if file_name.endswith(".csv"):

            return pd.read_csv(
                uploaded_file
            )


        # ====================================================
        # TSV
        # ====================================================

        elif file_name.endswith(".tsv"):

            return pd.read_csv(
                uploaded_file,
                sep="\t"
            )


        # ====================================================
        # EXCEL
        # ====================================================

        elif file_name.endswith(
            (".xlsx", ".xls")
        ):

            return pd.read_excel(
                uploaded_file
            )


        # ====================================================
        # UNSUPPORTED
        # ====================================================

        else:

            raise ValueError(
                "Unsupported file format. "
                "Please upload CSV, TSV or Excel."
            )

    except pd.errors.EmptyDataError:

        raise ValueError(
            "The uploaded file is empty."
        )

    except pd.errors.ParserError:

        raise ValueError(
            "Could not parse the file. "
            "Please check that the dataset is valid."
        )

    except Exception as e:

        raise ValueError(
            f"Error loading dataset: {str(e)}"
        )