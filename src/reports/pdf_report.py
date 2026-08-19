import os
from io import BytesIO
from datetime import datetime

import pandas as pd
import numpy as np

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
    KeepTogether
)


# ============================================================
# COLORS
# ============================================================

PRIMARY = colors.HexColor("#1F4E78")
SECONDARY = colors.HexColor("#D9EAF7")
LIGHT = colors.HexColor("#F4F7FA")
DARK = colors.HexColor("#222222")
GREY = colors.HexColor("#666666")
SUCCESS = colors.HexColor("#2E7D32")
WARNING = colors.HexColor("#C62828")


# ============================================================
# STYLES
# ============================================================

def get_styles():

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontSize=26,
            leading=32,
            alignment=TA_CENTER,
            textColor=PRIMARY,
            spaceAfter=15
        )
    )

    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["Normal"],
            fontSize=12,
            leading=18,
            alignment=TA_CENTER,
            textColor=GREY,
            spaceAfter=20
        )
    )

    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading1"],
            fontSize=17,
            leading=22,
            textColor=PRIMARY,
            spaceBefore=10,
            spaceAfter=12
        )
    )

    styles.add(
        ParagraphStyle(
            name="SubSection",
            parent=styles["Heading2"],
            fontSize=13,
            leading=18,
            textColor=DARK,
            spaceBefore=8,
            spaceAfter=8
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            textColor=DARK,
            spaceAfter=7
        )
    )

    styles.add(
        ParagraphStyle(
            name="Insight",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            leftIndent=10,
            spaceAfter=5
        )
    )

    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["Normal"],
            fontSize=8,
            leading=11,
            textColor=GREY
        )
    )

    return styles


# ============================================================
# SAFE VALUE
# ============================================================

def safe_text(value):

    if value is None:
        return ""

    try:

        if pd.isna(value):
            return ""

    except Exception:
        pass

    return str(value)


# ============================================================
# NUMBER FORMAT
# ============================================================

def format_number(value):

    try:

        value = float(value)

        if value.is_integer():

            return f"{int(value):,}"

        return f"{value:,.2f}"

    except Exception:

        return safe_text(value)


# ============================================================
# TABLE
# ============================================================

def create_table(
    data,
    col_widths=None,
    header=True
):

    table = Table(
        data,
        colWidths=col_widths,
        repeatRows=1 if header else 0
    )

    commands = [

        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.grey
        ),

        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),

        (
            "FONTNAME",
            (0, 0),
            (-1, -1),
            "Helvetica"
        ),

        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            8
        ),

        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),

        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),

        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            5
        ),

        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5
        )
    ]

    if header:

        commands.extend([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                PRIMARY
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            )

        ])

    table.setStyle(
        TableStyle(commands)
    )

    return table


# ============================================================
# DATASET OVERVIEW
# ============================================================

def overview_table(df):

    numerical = len(
        df.select_dtypes(
            include=np.number
        ).columns
    )

    categorical = len(
        df.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        ).columns
    )

    rows = [

        ["Metric", "Value"],

        [
            "Rows",
            format_number(df.shape[0])
        ],

        [
            "Columns",
            format_number(df.shape[1])
        ],

        [
            "Total Cells",
            format_number(
                df.shape[0] * df.shape[1]
            )
        ],

        [
            "Missing Values",
            format_number(
                df.isnull().sum().sum()
            )
        ],

        [
            "Duplicate Rows",
            format_number(
                df.duplicated().sum()
            )
        ],

        [
            "Numerical Columns",
            numerical
        ],

        [
            "Categorical Columns",
            categorical
        ]
    ]

    return create_table(
        rows,
        col_widths=[
            3.2 * inch,
            2.8 * inch
        ]
    )


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

def create_executive_summary(
    df,
    insights
):

    rows = df.shape[0]
    columns = df.shape[1]

    missing = int(
        df.isnull().sum().sum()
    )

    duplicates = int(
        df.duplicated().sum()
    )

    numeric = len(
        df.select_dtypes(
            include=np.number
        ).columns
    )

    categorical = len(
        df.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        ).columns
    )

    summary = []

    summary.append(
        f"The dataset contains {rows:,} rows "
        f"and {columns:,} columns."
    )

    summary.append(
        f"It contains {numeric} numerical "
        f"and {categorical} categorical columns."
    )

    if missing == 0:

        summary.append(
            "No missing values were detected."
        )

    else:

        summary.append(
            f"{missing:,} missing values were detected "
            "and should be reviewed."
        )

    if duplicates == 0:

        summary.append(
            "No duplicate records were detected."
        )

    else:

        summary.append(
            f"{duplicates:,} duplicate records "
            "were detected."
        )

    if insights:

        for category in [
            "correlations",
            "outliers"
        ]:

            items = insights.get(
                category,
                []
            )

            if items:

                summary.append(
                    safe_text(items[0])
                )

    return summary


# ============================================================
# MISSING VALUE TABLE
# ============================================================

def missing_table(df):

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

        return None

    rows = [
        [
            "Column",
            "Missing",
            "Percentage"
        ]
    ]

    for column, count in missing.items():

        percentage = (
            count / len(df)
        ) * 100

        rows.append(
            [
                safe_text(column),
                format_number(count),
                f"{percentage:.2f}%"
            ]
        )

    return create_table(
        rows,
        col_widths=[
            3 * inch,
            1.5 * inch,
            1.5 * inch
        ]
    )


# ============================================================
# NUMERICAL TABLE
# ============================================================

def numerical_table(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    if numeric.empty:

        return None

    description = (
        numeric.describe()
        .T
    )

    rows = [[
        "Column",
        "Mean",
        "Std",
        "Min",
        "Median",
        "Max"
    ]]

    for column, row in description.iterrows():

        median = numeric[
            column
        ].median()

        rows.append([
            safe_text(column),
            format_number(row["mean"]),
            format_number(row["std"]),
            format_number(row["min"]),
            format_number(median),
            format_number(row["max"])
        ])

    return create_table(
        rows,
        col_widths=[
            1.65 * inch,
            0.95 * inch,
            0.95 * inch,
            0.95 * inch,
            0.95 * inch,
            0.95 * inch
        ]
    )


# ============================================================
# CORRELATION TABLE
# ============================================================

def correlation_table(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    if numeric.shape[1] < 2:

        return None

    corr = numeric.corr()

    columns = list(
        corr.columns
    )

    # Avoid huge PDF tables

    if len(columns) > 10:

        columns = columns[:10]

        corr = corr.loc[
            columns,
            columns
        ]

    rows = [
        ["Variable"] + columns
    ]

    for row_name in columns:

        row = [row_name]

        for column in columns:

            value = corr.loc[
                row_name,
                column
            ]

            if pd.isna(value):

                row.append("N/A")

            else:

                row.append(
                    f"{value:.2f}"
                )

        rows.append(row)

    width = (
        6.5 / (len(columns) + 1)
    ) * inch

    return create_table(
        rows,
        col_widths=[
            width
            for _ in range(
                len(columns) + 1
            )
        ]
    )


# ============================================================
# INSIGHTS
# ============================================================

def add_insights(
    story,
    insights,
    styles
):

    if not insights:

        return

    titles = {

        "overview":
            "Dataset Overview",

        "missing":
            "Missing Values",

        "duplicates":
            "Duplicate Rows",

        "numerical":
            "Numerical Findings",

        "extreme_values":
            "Extreme Values",

        "correlations":
            "Correlation Findings",

        "outliers":
            "Outlier Findings",

        "categorical":
            "Categorical Findings",

        "constant_columns":
            "Constant Columns",

        "data_types":
            "Data Type Findings",

        "recommendations":
            "Recommendations"
    }

    for category, items in insights.items():

        if not items:

            continue

        title = titles.get(
            category,
            category.replace(
                "_",
                " "
            ).title()
        )

        story.append(
            Paragraph(
                title,
                styles["SubSection"]
            )
        )

        for item in items:

            story.append(
                Paragraph(
                    f"• {safe_text(item)}",
                    styles["Insight"]
                )
            )


# ============================================================
# VISUALIZATION
# ============================================================

def add_visualizations(
    story,
    saved_charts,
    styles
):

    if not saved_charts:

        story.append(
            Paragraph(
                "No visualizations were saved.",
                styles["BodyCustom"]
            )
        )

        return

    story.append(
        Paragraph(
            "Visualizations",
            styles["Section"]
        )
    )

    for index, chart in enumerate(
        saved_charts,
        start=1
    ):

        title = chart.get(
            "title",
            f"Visualization {index}"
        )

        image_data = chart.get(
            "image"
        )

        story.append(
            Paragraph(
                f"{index}. {safe_text(title)}",
                styles["SubSection"]
            )
        )

        if image_data is None:

            continue

        try:

            image = Image(
                BytesIO(image_data)
            )

            image.drawWidth = (
                6.4 * inch
            )

            image.drawHeight = (
                4.2 * inch
            )

            story.append(image)

        except Exception:

            story.append(
                Paragraph(
                    "Unable to display this chart.",
                    styles["Small"]
                )
            )

        story.append(
            Spacer(
                1,
                15
            )
        )


# ============================================================
# PAGE NUMBER
# ============================================================

def add_page_number(
    canvas,
    document
):

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.setFillColor(
        GREY
    )

    canvas.drawRightString(
        A4[0] - 40,
        20,
        f"Page {document.page}"
    )

    canvas.restoreState()


# ============================================================
# GENERATE PDF
# ============================================================

def generate_pdf_report(
    df,
    insights=None,
    saved_charts=None,
    cleaning_summary=None,
    file_name="dataset"
):

    buffer = BytesIO()

    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=40,

        leftMargin=40,

        topMargin=45,

        bottomMargin=35
    )

    styles = get_styles()

    story = []


    # ========================================================
    # COVER
    # ========================================================

    story.append(
        Spacer(
            1,
            1.2 * inch
        )
    )

    story.append(
        Paragraph(
            "SMART DATA ANALYZER",
            styles["CoverTitle"]
        )
    )

    story.append(
        Paragraph(
            "Automated Data Analysis Report",
            styles["CoverSubtitle"]
        )
    )

    story.append(
        Spacer(
            1,
            20
        )
    )

    cover_data = [

        ["Dataset", safe_text(file_name)],

        [
            "Generated",
            datetime.now().strftime(
                "%d %B %Y, %H:%M"
            )
        ],

        [
            "Rows",
            format_number(
                len(df)
            )
        ],

        [
            "Columns",
            format_number(
                len(df.columns)
            )
        ]
    ]

    story.append(
        create_table(
            cover_data,
            col_widths=[
                2 * inch,
                4 * inch
            ],
            header=False
        )
    )

    story.append(
        Spacer(
            1,
            30
        )
    )

    story.append(
        Paragraph(
            "This report was automatically generated "
            "by Smart Data Analyzer. It summarizes "
            "data quality, statistical characteristics, "
            "relationships, insights, visualizations, "
            "and recommendations.",
            styles["BodyCustom"]
        )
    )

    story.append(
        PageBreak()
    )


    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "Executive Summary",
            styles["Section"]
        )
    )

    summary = create_executive_summary(
        df,
        insights
    )

    for item in summary:

        story.append(
            Paragraph(
                f"• {safe_text(item)}",
                styles["Insight"]
            )
        )

    story.append(
        Spacer(
            1,
            10
        )
    )


    # ========================================================
    # DATASET OVERVIEW
    # ========================================================

    story.append(
        Paragraph(
            "1. Dataset Overview",
            styles["Section"]
        )
    )

    story.append(
        overview_table(df)
    )


    # ========================================================
    # DATA QUALITY
    # ========================================================

    story.append(
        Paragraph(
            "2. Data Quality Analysis",
            styles["Section"]
        )
    )

    missing = missing_table(df)

    if missing is None:

        story.append(
            Paragraph(
                "✅ No missing values were detected.",
                styles["BodyCustom"]
            )
        )

    else:

        story.append(missing)

    story.append(
        Spacer(
            1,
            10
        )
    )

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count == 0:

        text = (
            "✅ No duplicate rows were detected."
        )

    else:

        text = (
            f"⚠️ {duplicate_count:,} "
            "duplicate rows were detected."
        )

    story.append(
        Paragraph(
            text,
            styles["BodyCustom"]
        )
    )


    # ========================================================
    # CLEANING
    # ========================================================

    if cleaning_summary:

        story.append(
            Paragraph(
                "3. Cleaning Summary",
                styles["Section"]
            )
        )

        if isinstance(
            cleaning_summary,
            dict
        ):

            rows = [
                [
                    "Operation",
                    "Result"
                ]
            ]

            for key, value in (
                cleaning_summary.items()
            ):

                rows.append([
                    safe_text(key),
                    safe_text(value)
                ])

            story.append(
                create_table(
                    rows,
                    col_widths=[
                        3.5 * inch,
                        2.5 * inch
                    ]
                )
            )

        else:

            story.append(
                Paragraph(
                    safe_text(
                        cleaning_summary
                    ),
                    styles["BodyCustom"]
                )
            )


    # ========================================================
    # STATISTICAL ANALYSIS
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "4. Statistical Analysis",
            styles["Section"]
        )
    )

    statistics = numerical_table(df)

    if statistics is None:

        story.append(
            Paragraph(
                "No numerical columns were found.",
                styles["BodyCustom"]
            )
        )

    else:

        story.append(
            statistics
        )


    # ========================================================
    # CORRELATION
    # ========================================================

    story.append(
        Spacer(
            1,
            20
        )
    )

    story.append(
        Paragraph(
            "5. Correlation Analysis",
            styles["Section"]
        )
    )

    corr = correlation_table(df)

    if corr is None:

        story.append(
            Paragraph(
                "At least two numerical columns "
                "are required.",
                styles["BodyCustom"]
            )
        )

    else:

        story.append(corr)


    # ========================================================
    # INSIGHTS
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "6. Automatic Insights",
            styles["Section"]
        )
    )

    add_insights(
        story,
        insights,
        styles
    )


    # ========================================================
    # VISUALIZATIONS
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "7. Visualizations",
            styles["Section"]
        )
    )

    add_visualizations(
        story,
        saved_charts,
        styles
    )


    # ========================================================
    # CONCLUSION
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "8. Conclusion",
            styles["Section"]
        )
    )

    story.append(
        Paragraph(
            "The Smart Data Analyzer provides an "
            "automated overview of the uploaded dataset, "
            "including data quality, statistical "
            "characteristics, relationships, visual "
            "patterns, and automatically detected "
            "insights.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "The generated findings should be reviewed "
            "using domain knowledge before being used "
            "for important business decisions or "
            "machine-learning applications.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Spacer(
            1,
            20
        )
    )

    story.append(
        Paragraph(
            "Generated by Smart Data Analyzer",
            styles["CoverSubtitle"]
        )
    )


    # ========================================================
    # BUILD
    # ========================================================

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    buffer.seek(0)

    return buffer.getvalue()