#!/usr/bin/env python3
"""
Data Quality Assessment for Cross Platform Job Analytics
Generates a markdown report with key data quality metrics.
"""
from __future__ import annotations
import argparse
import os
import sys
from datetime import datetime
import pandas as pd

DEFAULT_INPUT = os.path.join('data', 'raw', 'unified_jobs_dataset.csv')
DEFAULT_REPORT = os.path.join('reports', 'data_cleaning_report.md')

KEY_FIELDS = [
    'title', 'company', 'city', 'category_searched', 'salary_text',
    'skills', 'experience_text', 'description', 'job_type', 'posting_date_text',
    'job_url', 'source'
]


def safe_value_counts(df: pd.DataFrame, col: str, n: int = 15) -> str:
    if col in df.columns:
        vc = df[col].astype(str).value_counts(dropna=True).head(n)
        return vc.to_string()
    return f"Column '{col}' not found."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=DEFAULT_INPUT, help='Path to raw dataset CSV')
    parser.add_argument('--output', default=DEFAULT_REPORT, help='Path to markdown report')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Loading dataset: {args.input}")
    try:
        df = pd.read_csv(args.input)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        sys.exit(1)

    n_rows, n_cols = df.shape

    # Duplicates by job_url if present else by title+company
    if 'job_url' in df.columns:
        dup_count = df.duplicated(subset=['job_url']).sum()
    else:
        subset = [c for c in ['title', 'company'] if c in df.columns]
        dup_count = df.duplicated(subset=subset).sum() if subset else 0

    missing_series = df.isnull().sum().sort_values(ascending=False)

    # Build markdown report
    lines = []
    lines.append(f"# Data Quality Report")
    lines.append("")
    lines.append(f"## Dataset Overview")
    lines.append(f"- Shape: {n_rows} rows × {n_cols} columns")
    lines.append(f"- Duplicates: {dup_count}")
    lines.append("")

    lines.append("## Missing Values (Top 20)")
    lines.append("```")
    lines.append(missing_series.head(20).to_string())
    lines.append("```")

    lines.append("## Dtypes")
    lines.append("```")
    lines.append(df.dtypes.to_string())
    lines.append("```")

    # Distributions for key fields
    for col in ['salary_text', 'experience_text', 'job_type', 'city', 'category_searched', 'source']:
        lines.append(f"## Distribution: {col}")
        lines.append("```")
        lines.append(safe_value_counts(df, col))
        lines.append("```")

    # Sample rows
    sample_cols = [c for c in ['title', 'company', 'city', 'salary_text', 'experience_text', 'job_type', 'source'] if c in df.columns]
    if sample_cols:
        lines.append("## Sample Rows")
        lines.append("```")
        lines.append(df[sample_cols].head(10).to_string(index=False))
        lines.append("```")

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"Report written to: {args.output}")


if __name__ == '__main__':
    main()
