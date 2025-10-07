#!/usr/bin/env python3
"""
Data Preprocessing for Cross Platform Job Analytics (Phase 2.5)
- Loads cleaned dataset
- Builds feature-ready dataset:
  - One-hot skills for top-N skills
  - Encodes categorical columns (source, job_type, location_tier)
  - Keeps numeric salary/experience features
- Saves features CSV and appends summary to report
"""
from __future__ import annotations
import argparse
import os
from datetime import datetime
import pandas as pd
import numpy as np
from collections import Counter

DEFAULT_INPUT = os.path.join('data', 'processed', 'cleaned_jobs_dataset.csv')
DEFAULT_OUTPUT = os.path.join('data', 'processed', 'features_jobs_dataset.csv')
DEFAULT_REPORT = os.path.join('reports', 'data_cleaning_report.md')


def extract_top_skills(df: pd.DataFrame, skills_col: str = 'skills_clean', top_n: int = 30) -> list[str]:
    counter = Counter()
    if skills_col in df.columns:
        for s in df[skills_col].dropna():
            for sk in [p.strip() for p in str(s).split(',') if p.strip()]:
                counter[sk] += 1
    return [sk for sk, _ in counter.most_common(top_n)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=DEFAULT_INPUT)
    parser.add_argument('--output', default=DEFAULT_OUTPUT)
    parser.add_argument('--report', default=DEFAULT_REPORT)
    parser.add_argument('--top_skills', type=int, default=30)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Loading cleaned dataset: {args.input}")
    df = pd.read_csv(args.input)

    # Identify top skills
    top_skills = extract_top_skills(df, 'skills_clean', top_n=args.top_skills)

    # Prepare base features
    feature_cols = {}

    # Salary & experience numeric features (already numeric)
    for col in ['min_salary_inr', 'max_salary_inr', 'avg_salary_inr', 'avg_salary_inr_capped', 'avg_salary_lpa', 'avg_salary_lpa_capped', 'exp_min_years', 'exp_max_years']:
        if col in df.columns:
            feature_cols[col] = df[col]
    # Log salary features
    if 'avg_salary_inr' in df.columns:
        feature_cols['log_avg_salary'] = df['avg_salary_inr'].apply(lambda x: np.log1p(x) if pd.notna(x) and x > 0 else np.nan)
    if 'avg_salary_inr_capped' in df.columns:
        feature_cols['log_avg_salary_capped'] = df['avg_salary_inr_capped'].apply(lambda x: np.log1p(x) if pd.notna(x) and x > 0 else np.nan)

    # Experience level as ordinal mapping
    level_map = {'Entry': 0, 'Junior': 1, 'Mid': 2, 'Senior': 3}
    if 'experience_level' in df.columns:
        feature_cols['experience_level_code'] = df['experience_level'].map(level_map)

    # Salary bands (in LPA)
    if 'avg_salary_lpa' in df.columns:
        def band(v):
            if pd.isna(v):
                return np.nan
            if v < 3: return '<3 LPA'
            if v < 6: return '3-6 LPA'
            if v < 10: return '6-10 LPA'
            if v < 20: return '10-20 LPA'
            return '>=20 LPA'
        bands = df['avg_salary_lpa'].apply(band)
        dummies = pd.get_dummies(bands, prefix='salary_band', dtype=int)
        for c in dummies.columns:
            feature_cols[c] = dummies[c]

    # Categorical encodings
    # Source, job_type, location_tier
    for cat_col in ['source', 'job_type', 'location_tier']:
        if cat_col in df.columns:
            dummies = pd.get_dummies(df[cat_col].fillna('Unknown'), prefix=cat_col, dtype=int)
            for c in dummies.columns:
                feature_cols[c] = dummies[c]

    # Skills one-hot for top-N skills (case-insensitive)
    for sk in top_skills:
        col_name = f"skill_{sk.replace(' ', '_').replace('/', '_')}"
        feature_cols[col_name] = df['skills_clean'].fillna('').apply(lambda s, target=sk.lower(): 1 if any(p.strip().lower()==target for p in s.split(',')) else 0)

    # Assemble feature dataframe
    feat_df = pd.DataFrame(feature_cols)

    # Optionally keep identifiers for traceability
    keep_ids = [c for c in ['job_id', 'title_clean', 'company_clean', 'city_clean', 'category_searched_clean'] if c in df.columns]
    if keep_ids:
        feat_df = pd.concat([df[keep_ids], feat_df], axis=1)

    feat_df.to_csv(args.output, index=False)
    print(f"Saved features dataset: {args.output} ({len(feat_df)} rows, {feat_df.shape[1]} columns)")

    # Append summary to report
    lines = []
    lines.append("\n---\n")
    lines.append("## Preprocessing Summary")
    lines.append(f"Top skills used: {', '.join(top_skills)}")
    lines.append(f"Feature columns: {feat_df.shape[1]}")

    with open(args.report, 'a', encoding='utf-8') as f:
        f.write("\n".join(lines))


if __name__ == '__main__':
    main()
