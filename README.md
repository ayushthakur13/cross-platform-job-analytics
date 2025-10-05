# Cross Platform Job Analytics (Single-Source Edition)

## Overview
This project aggregates and analyzes Indian tech job postings from a single reliable source (Internshala) to uncover trends in roles, skills, locations, and salaries. Other platforms were excluded due to access limitations, so the pipeline is optimized for Internshala data end-to-end.

---

## Objectives
- Collect real-time job data from Internshala
- Clean and standardize the dataset (columns, salaries, dates, locations)
- Prepare a feature-ready dataset for analysis and ML
- Perform Exploratory Data Analysis (EDA) to visualize key insights

---

## Tech Stack

| Category         | Tools / Libraries                |
|------------------|----------------------------------|
| Language         | Python 3.11                      |
| Data Collection  | requests, BeautifulSoup          |
| Data Processing  | pandas, numpy                    |
| Visualization    | matplotlib, seaborn, plotly      |
| Storage          | CSV                              |
| Environment      | venv (virtual environment)       |

---

## Project Structure

cross-platform-job-analytics/
├── data/
│   ├── raw/               # Raw scraped data (CSV snapshots)
│   └── processed/         # Cleaned and feature datasets for analysis
├── notebooks/             # (optional) Jupyter notebooks for EDA
├── reports/
│   └── data_cleaning_report.md
├── scripts/
│   ├── data_cleaning.py
│   ├── data_preprocessing.py
│   ├── data_quality_assessment.py
│   └── salary_parser.py
├── src/
│   └── scraping/
│       └── internshala_optimized.py
├── collect_complete_data.py
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore

---

## Notes
- This repository intentionally focuses on a single data source (Internshala) for reliability.
- Reports and the data dictionary are updated as you run the cleaning and preprocessing scripts.
