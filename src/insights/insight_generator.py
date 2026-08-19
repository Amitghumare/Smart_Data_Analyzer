import pandas as pd
import numpy as np


# ============================================================
# COLUMN HELPERS
# ============================================================

def get_numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def get_categorical_columns(df):

    return df.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    ).columns.tolist()


# ============================================================
# DATASET OVERVIEW INSIGHTS
# ============================================================

def generate_overview_insights(df):

    insights = []

    rows = df.shape[0]
    columns = df.shape[1]

    numeric_columns = get_numeric_columns(df)
    categorical_columns = get_categorical_columns(df)

    insights.append(
        f"The dataset contains {rows:,} rows "
        f"and {columns:,} columns."
    )

    insights.append(
        f"There are {len(numeric_columns)} numerical "
        f"columns and {len(categorical_columns)} "
        f"categorical columns."
    )

    if rows > 100000:

        insights.append(
            "The dataset is relatively large and "
            "may require optimized processing."
        )

    elif rows < 1000:

        insights.append(
            "The dataset is relatively small, so "
            "statistical conclusions should be interpreted carefully."
        )

    return insights


# ============================================================
# MISSING VALUE INSIGHTS
# ============================================================

def generate_missing_insights(df):

    insights = []

    missing = (
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
    )

    missing = missing[
        missing > 0
    ]

    if missing.empty:

        insights.append(
            "No missing values were detected "
            "in the dataset."
        )

        return insights

    total_rows = len(df)

    for column, count in missing.items():

        percentage = (
            count / total_rows
        ) * 100

        if percentage >= 50:

            insights.append(
                f"'{column}' has {percentage:.1f}% "
                f"missing values. This column should "
                f"be reviewed carefully before modeling."
            )

        elif percentage >= 20:

            insights.append(
                f"'{column}' has {percentage:.1f}% "
                f"missing values, which may affect analysis."
            )

        else:

            insights.append(
                f"'{column}' has {count:,} missing "
                f"values ({percentage:.1f}%)."
            )

    return insights


# ============================================================
# DUPLICATE INSIGHTS
# ============================================================

def generate_duplicate_insights(df):

    insights = []

    duplicates = int(
        df.duplicated().sum()
    )

    if duplicates == 0:

        insights.append(
            "No duplicate rows were detected."
        )

        return insights

    percentage = (
        duplicates / len(df)
    ) * 100

    insights.append(
        f"The dataset contains {duplicates:,} "
        f"duplicate rows ({percentage:.2f}% of the dataset)."
    )

    if percentage > 10:

        insights.append(
            "A relatively high percentage of duplicate "
            "rows was detected. Removing duplicates "
            "should be considered."
        )

    return insights


# ============================================================
# NUMERICAL STATISTICAL INSIGHTS
# ============================================================

def generate_numerical_insights(df):

    insights = []

    numeric_columns = (
        get_numeric_columns(df)
    )

    if not numeric_columns:

        insights.append(
            "No numerical columns were found "
            "for statistical analysis."
        )

        return insights

    for column in numeric_columns:

        series = (
            pd.to_numeric(
                df[column],
                errors="coerce"
            )
            .dropna()
        )

        if series.empty:

            continue

        minimum = series.min()
        maximum = series.max()
        mean = series.mean()
        median = series.median()

        insights.append(
            f"'{column}' ranges from "
            f"{minimum:.2f} to {maximum:.2f}, "
            f"with a mean of {mean:.2f} "
            f"and median of {median:.2f}."
        )

        if mean > median * 1.2:

            insights.append(
                f"'{column}' appears to be "
                f"right-skewed because the mean "
                f"is considerably higher than the median."
            )

        elif (
            median != 0
            and mean < median * 0.8
        ):

            insights.append(
                f"'{column}' may be left-skewed "
                f"because the mean is considerably "
                f"lower than the median."
            )

    return insights


# ============================================================
# EXTREME VALUE INSIGHTS
# ============================================================

def generate_extreme_value_insights(df):

    insights = []

    numeric_columns = (
        get_numeric_columns(df)
    )

    for column in numeric_columns:

        series = (
            pd.to_numeric(
                df[column],
                errors="coerce"
            )
            .dropna()
        )

        if series.empty:

            continue

        max_value = series.max()
        min_value = series.min()

        max_count = int(
            (series == max_value).sum()
        )

        min_count = int(
            (series == min_value).sum()
        )

        insights.append(
            f"'{column}' has a maximum value "
            f"of {max_value:.2f}."
        )

        insights.append(
            f"'{column}' has a minimum value "
            f"of {min_value:.2f}."
        )

        if max_count == 1:

            insights.append(
                f"The maximum value of '{column}' "
                f"occurs only once."
            )

    return insights


# ============================================================
# CORRELATION INSIGHTS
# ============================================================

def generate_correlation_insights(
    df,
    threshold=0.7
):

    insights = []

    numeric_columns = (
        get_numeric_columns(df)
    )

    if len(numeric_columns) < 2:

        return insights

    correlation = (
        df[numeric_columns]
        .corr(
            numeric_only=True
        )
    )

    columns = correlation.columns

    found_strong = False

    for i in range(
        len(columns)
    ):

        for j in range(
            i + 1,
            len(columns)
        ):

            col1 = columns[i]
            col2 = columns[j]

            value = correlation.loc[
                col1,
                col2
            ]

            if pd.isna(value):

                continue

            if abs(value) >= threshold:

                found_strong = True

                direction = (
                    "positive"
                    if value > 0
                    else "negative"
                )

                strength = (
                    "strong"
                    if abs(value) >= 0.8
                    else "moderate-to-strong"
                )

                insights.append(
                    f"'{col1}' and '{col2}' "
                    f"have a {strength} {direction} "
                    f"correlation of {value:.2f}."
                )

    if not found_strong:

        insights.append(
            "No strong correlations above the "
            f"{threshold:.1f} threshold were detected."
        )

    return insights


# ============================================================
# OUTLIER INSIGHTS
# ============================================================

def generate_outlier_insights(df):

    insights = []

    numeric_columns = (
        get_numeric_columns(df)
    )

    for column in numeric_columns:

        series = (
            pd.to_numeric(
                df[column],
                errors="coerce"
            )
            .dropna()
        )

        if len(series) < 5:

            continue

        q1 = series.quantile(
            0.25
        )

        q3 = series.quantile(
            0.75
        )

        iqr = q3 - q1

        if iqr == 0:

            continue

        lower = (
            q1 - 1.5 * iqr
        )

        upper = (
            q3 + 1.5 * iqr
        )

        outliers = (
            (series < lower)
            |
            (series > upper)
        )

        count = int(
            outliers.sum()
        )

        if count == 0:

            continue

        percentage = (
            count / len(series)
        ) * 100

        insights.append(
            f"'{column}' contains {count:,} "
            f"potential outliers ({percentage:.2f}%)."
        )

        if percentage > 5:

            insights.append(
                f"'{column}' has a relatively high "
                f"outlier percentage and should be "
                f"investigated before modeling."
            )

    if not insights:

        insights.append(
            "No significant IQR-based outlier "
            "patterns were detected."
        )

    return insights


# ============================================================
# CATEGORICAL INSIGHTS
# ============================================================

def generate_categorical_insights(df):

    insights = []

    categorical_columns = (
        get_categorical_columns(df)
    )

    for column in categorical_columns:

        series = (
            df[column]
            .dropna()
        )

        if series.empty:

            continue

        unique_count = (
            series.nunique()
        )

        if unique_count == 1:

            insights.append(
                f"'{column}' contains only one "
                f"unique value and may not provide "
                f"useful analytical information."
            )

            continue

        value_counts = (
            series
            .value_counts()
        )

        top_category = (
            value_counts.index[0]
        )

        top_count = (
            value_counts.iloc[0]
        )

        top_percentage = (
            top_count
            / len(series)
            * 100
        )

        insights.append(
            f"'{column}' contains {unique_count:,} "
            f"unique categories. The most common "
            f"category is '{top_category}' "
            f"({top_percentage:.1f}% of non-null values)."
        )

        if top_percentage > 80:

            insights.append(
                f"'{column}' is highly dominated by "
                f"'{top_category}', which may indicate "
                f"class imbalance."
            )

    return insights


# ============================================================
# CONSTANT COLUMN INSIGHTS
# ============================================================

def generate_constant_column_insights(df):

    insights = []

    for column in df.columns:

        unique_count = (
            df[column]
            .nunique(
                dropna=False
            )
        )

        if unique_count <= 1:

            insights.append(
                f"'{column}' contains only one "
                f"unique value and can potentially "
                f"be removed."
            )

    return insights


# ============================================================
# DATA TYPE INSIGHTS
# ============================================================

def generate_dtype_insights(df):

    insights = []

    for column in df.columns:

        dtype = df[column].dtype

        if dtype == "object":

            # Check if object might actually be numeric

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            valid_ratio = (
                converted.notna().mean()
            )

            if valid_ratio > 0.9:

                insights.append(
                    f"'{column}' is stored as text "
                    f"but appears to contain mostly "
                    f"numeric values. Consider converting "
                    f"its data type."
                )

    return insights


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(df):

    recommendations = []

    missing_total = int(
        df.isnull()
        .sum()
        .sum()
    )

    duplicates = int(
        df.duplicated()
        .sum()
    )

    numeric_columns = (
        get_numeric_columns(df)
    )

    categorical_columns = (
        get_categorical_columns(df)
    )

    # Missing values

    if missing_total > 0:

        recommendations.append(
            "Review missing values and choose an "
            "appropriate imputation or removal strategy."
        )

    # Duplicates

    if duplicates > 0:

        recommendations.append(
            "Review duplicate records before performing "
            "advanced analysis or machine learning."
        )

    # Numerical data

    if numeric_columns:

        recommendations.append(
            "Use distributions, box plots, and correlation "
            "analysis to understand numerical variables."
        )

    # Categorical data

    if categorical_columns:

        recommendations.append(
            "Analyze category frequencies and investigate "
            "highly imbalanced categorical variables."
        )

    # Dataset size

    if len(df) < 100:

        recommendations.append(
            "The dataset is small. Avoid making strong "
            "generalizations from the observed patterns."
        )

    recommendations.append(
        "Validate important findings with domain knowledge "
        "before using them for business decisions."
    )

    return recommendations


# ============================================================
# GENERATE ALL INSIGHTS
# ============================================================

def generate_all_insights(df):

    result = {

        "overview":
            generate_overview_insights(df),

        "missing":
            generate_missing_insights(df),

        "duplicates":
            generate_duplicate_insights(df),

        "numerical":
            generate_numerical_insights(df),

        "extreme_values":
            generate_extreme_value_insights(df),

        "correlations":
            generate_correlation_insights(df),

        "outliers":
            generate_outlier_insights(df),

        "categorical":
            generate_categorical_insights(df),

        "constant_columns":
            generate_constant_column_insights(df),

        "data_types":
            generate_dtype_insights(df),

        "recommendations":
            generate_recommendations(df)
    }

    return result


# ============================================================
# FLATTEN INSIGHTS
# ============================================================

def flatten_insights(
    insights_dict
):

    insights = []

    for category, items in (
        insights_dict.items()
    ):

        if not isinstance(
            items,
            list
        ):

            continue

        for item in items:

            insights.append({

                "category":
                    category,

                "insight":
                    item
            })

    return insights