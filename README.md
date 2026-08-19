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
│   │
│   └── processed/
│       └── .gitkeep
│
├── src/
│   │
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



                  USER
                │
                ▼
        ┌───────────────┐
        │ Upload Dataset│
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ Data Loader   │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │   Overview    │
        └───────┬───────┘
                │
        ┌───────┴────────┐
        ▼                ▼
   Data Cleaning       EDA
        │                │
        └───────┬────────┘
                ▼
        Visualization
                │
                ▼
           Insights
                │
                ▼
             Report
                │
                ▼
            Download


for models download


            python -c "from src.session.state import initialize_session_state; from src.data_loader.loader import load_dataset; from src.utils.validator import validate_dataset; print('All imports OK')"