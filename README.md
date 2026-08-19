# 📊 Smart Data Analyzer

An end-to-end data analysis application designed to simplify the process of **dataset exploration, data cleaning, exploratory data analysis (EDA), visualization, statistical insights, and report generation**.

The project provides a modular architecture where users can upload a dataset and move through a complete data-analysis workflow from raw data to downloadable reports.

---

## 🚀 Features

### 📂 1. Dataset Upload & Loading

* Upload and load datasets through the application.
* Dedicated data-loading module for handling input datasets.
* Dataset validation before analysis.

### 📋 2. Data Overview

Provides a quick overview of the uploaded dataset, including:

* Dataset structure
* Number of rows and columns
* Data types
* Basic statistics
* Dataset-level information

### 🧹 3. Data Cleaning

The project contains separate modules for common data-cleaning operations:

* Missing-value handling
* Duplicate detection
* Outlier detection
* Data-type handling
* Text cleaning

This modular approach makes the cleaning pipeline easier to maintain and extend.

### 🔍 4. Exploratory Data Analysis

The EDA module is divided into:

* **Univariate Analysis**
* **Bivariate Analysis**
* **Multivariate Analysis**
* **Correlation Analysis**

These components help identify patterns, relationships, distributions, and correlations within the dataset.

### 📈 5. Data Visualization

The visualization layer contains modules for:

* Static charts
* Interactive visualizations

Charts can be generated as part of the analysis workflow and stored in the project's output directory.

### 💡 6. Automated Insights

The project includes an insights module for generating:

* Statistical insights
* Data-driven recommendations

This helps transform raw analysis results into information that can be easier to interpret and act upon.

### 📑 7. Report Generation

The reporting module is responsible for generating analysis reports using:

* Report generation utilities
* HTML report templates
* Generated report output

---

## 🏗️ Project Architecture

```text
User
  │
  ▼
┌─────────────────────┐
│   Upload Dataset    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Data Loader     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Overview       │
└──────────┬──────────┘
           │
      ┌────┴────┐
      ▼         ▼
┌──────────┐ ┌──────────┐
│ Cleaning │ │   EDA    │
└────┬─────┘ └────┬─────┘
     │             │
     └──────┬──────┘
            ▼
   ┌─────────────────┐
   │ Visualization   │
   └────────┬────────┘
            ▼
   ┌─────────────────┐
   │    Insights     │
   └────────┬────────┘
            ▼
   ┌─────────────────┐
   │     Report      │
   └────────┬────────┘
            ▼
   ┌─────────────────┐
   │     Download    │
   └─────────────────┘
```

The complete workflow follows the project's documented flow from dataset upload through data loading, overview, cleaning/EDA, visualization, insights, reporting, and download.

---

## 📁 Project Structure

```text
smart-data-analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
│
├── src/
│   ├── __init__.py
│   │
│   ├── data_loader/
│   │   ├── __init__.py
│   │   └── loader.py
│   │
│   ├── cleaning/
│   │   ├── __init__.py
│   │   ├── missing_values.py
│   │   ├── duplicates.py
│   │   ├── outliers.py
│   │   ├── data_types.py
│   │   └── text_cleaning.py
│   │
│   ├── profiling/
│   │   ├── __init__.py
│   │   ├── overview.py
│   │   └── statistics.py
│   │
│   ├── eda/
│   │   ├── __init__.py
│   │   ├── univariate.py
│   │   ├── bivariate.py
│   │   ├── multivariate.py
│   │   └── correlation.py
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   └── interactive.py
│   │
│   ├── insights/
│   │   ├── __init__.py
│   │   ├── statistical.py
│   │   └── recommendations.py
│   │
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── templates/
│   │       └── report.html
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       ├── helpers.py
│       └── logger.py
│
├── pages/
│   ├── 01_📊_Overview.py
│   ├── 02_🧹_Cleaning.py
│   ├── 03_🔍_EDA.py
│   ├── 04_📈_Visualization.py
│   ├── 05_💡_Insights.py
│   └── 06_📑_Reports.py
│
├── outputs/
│   ├── charts/
│   ├── reports/
│   └── datasets/
│
└── logs/
    └── app.log
```

This structure is based directly on the uploaded project specification.

---

## 🛠️ Tech Stack

The provided project structure indicates a Python-based application with:

* **Python**
* **Streamlit** — application interface
* **Pandas** — data manipulation
* **Data analysis & statistics**
* **Data visualization**
* **HTML** — report templates
* Modular Python architecture

> Note: The uploaded project specification does not provide the exact contents of `requirements.txt`, so the complete dependency list cannot be confirmed from the provided source.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Amitghumare/smart-data-analyzer.git
cd smart-data-analyzer
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Then open the local URL displayed by Streamlit in your browser.

---

## 🧪 Verify the Project

The project specification includes an import-validation command:

```bash
python -c "from src.session.state import initialize_session_state; from src.data_loader.loader import load_dataset; from src.utils.validator import validate_dataset; print('All imports OK')"
```

This can be used as a quick check that the relevant project imports are working.

> **Important:** The provided project tree does not show `src/session/state.py` or `src/utils/validator.py`; it shows `src/utils/validators.py`. Therefore, this verification command may need to be updated to match the actual implementation.

---

## 📊 Application Pages

The application is divided into six primary pages:

| Page             | Purpose                                  |
| ---------------- | ---------------------------------------- |
| 📊 Overview      | Dataset overview and statistics          |
| 🧹 Cleaning      | Data-cleaning operations                 |
| 🔍 EDA           | Exploratory data analysis                |
| 📈 Visualization | Charts and interactive visualizations    |
| 💡 Insights      | Statistical insights and recommendations |
| 📑 Reports       | Generate and download reports            |

These pages correspond to the page modules defined in the project structure.

---

## 📤 Output

Generated artifacts are organized into:

```text
outputs/
├── charts/
├── reports/
└── datasets/
```

Application logs are stored under:

```text
logs/
└── app.log
```

---

## 🔄 How It Works

1. Upload a dataset.
2. The **Data Loader** loads the dataset.
3. The **Overview** page provides an initial understanding of the data.
4. Clean the dataset using the available cleaning modules.
5. Perform univariate, bivariate, multivariate, and correlation analysis.
6. Generate visualizations.
7. Generate statistical insights and recommendations.
8. Create an HTML report.
9. Download the generated results.

---

## 🎯 Use Cases

Smart Data Analyzer can be useful for:

* Data analysts
* Data science students
* Machine learning practitioners
* Exploratory data analysis
* Dataset quality checks
* Data-cleaning workflows
* Quick statistical analysis
* Automated analytical reporting

---

## 🔮 Future Improvements

Potential improvements for the project include:

* Support for additional file formats such as Excel and JSON
* More advanced automated EDA
* Machine-learning model integration
* Automated feature engineering
* AI-powered natural-language insights
* More interactive dashboards
* Export to PDF
* Database connectivity
* User authentication
* Cloud deployment
* Dataset comparison
* Advanced anomaly detection

---

## 📄 License

This project is intended for educational and development purposes.

If you plan to publish the project publicly, add an appropriate open-source license such as MIT License.

---

## 👨‍💻 Author

**Amit Ghumare**

Data Scientist | AI & ML Enthusiast

---

⭐ If you find this project useful, consider giving the repository a star!
