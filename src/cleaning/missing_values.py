import pandas as pd

def get_missing_summary(df):
    missing_count = df.isnull().sum()
    missing_percentage = (missing_count/ len(df) *100).round(2)

    summary = pd.DataFrame({"Missing Values": missing_count, "Missing Percentage": missing_percentage})

    return summary


def handle_missing_values(df,column, method, custom_value=None):
    df = df.copy()

    if method == "Mean":
        df[column] = df[column].fillna*(df[column].mean())

    elif method == "Median":
        df[column] = df[column].fillna(df[column].median())

    elif method == "Mode":
        mode_value=df[column].mode()

        if not mode_value.empty:
            df[column]= df[column].fillna(mode_value[0])

        elif method == "Forward Fill":
            df[column] = df[column].ffill()

        elif method == "Backward Fill":
            df[column] = df[column].bfill()

        elif method == "Custom Value":
            df[column] = df[column].fillna(custom_value)

        elif method == "Drop Rows":
            df= df.dropna(subset=[column])

        return df

    