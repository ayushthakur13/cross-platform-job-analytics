#!/usr/bin/env python3
"""
Generate EDA figures and append an EDA summary (date-less, path-less).
Inputs:
- data/processed/cleaned_jobs_dataset.csv
Outputs:
- reports/figures/*.png
- Appends an "## EDA Summary" section to reports/data_cleaning_report.md
"""
from __future__ import annotations
import os
import sys
import math
import subprocess
from typing import List

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

CLEANED = os.path.join('data', 'processed', 'cleaned_jobs_dataset.csv')
REPORT = os.path.join('reports', 'data_cleaning_report.md')
FIGDIR = os.path.join('reports', 'figures')

TOP_CITIES = 10
TOP_COMPANIES = 15
TOP_CATEGORIES = 15
TOP_SKILLS = 20
CO_SKILLS = 15

sns.set_theme(style="whitegrid")


def ensure_cleaned_ready():
    """Ensure cleaned dataset exists and is reasonable; if not, try to regenerate."""
    if not os.path.exists(CLEANED) or os.path.getsize(CLEANED) == 0:
        # Attempt to regenerate from raw
        raw = os.path.join('data', 'raw', 'unified_jobs_dataset.csv')
        if os.path.exists(raw):
            subprocess.run([sys.executable, os.path.join('scripts', 'data_cleaning.py'), '--input', raw, '--output', CLEANED, '--report', REPORT], check=True)
        else:
            raise FileNotFoundError("Raw dataset not found; cannot run EDA.")


def savefig(name: str):
    os.makedirs(FIGDIR, exist_ok=True)
    path = os.path.join(FIGDIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches='tight')
    plt.close()
    return path


def split_skills(s: str) -> List[str]:
    if not isinstance(s, str) or not s.strip():
        return []
    return [p.strip() for p in s.split(',') if p.strip()]


def eda():
    ensure_cleaned_ready()
    df = pd.read_csv(CLEANED)

    # Basic safe casts
    if 'avg_salary_inr' in df.columns:
        # avoid non-positive for log plots
        df['avg_salary_inr_pos'] = df['avg_salary_inr'].where(df['avg_salary_inr'] > 0)

    # 1) Salary distribution
    if 'avg_salary_inr_pos' in df.columns and df['avg_salary_inr_pos'].notna().any():
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.histplot(df['avg_salary_inr_pos'].dropna(), bins=40, kde=True, ax=ax)
        ax.set_xscale('log')
        ax.set_xlabel('Avg Salary (INR, log scale)')
        ax.set_title('Salary Distribution')
        savefig('salary_distribution.png')

    # 2) Salary by city (top cities by count)
    city_col = 'city_clean' if 'city_clean' in df.columns else ('city' if 'city' in df.columns else None)
    if city_col and 'avg_salary_inr_pos' in df.columns:
        top_cities = df[city_col].value_counts().head(TOP_CITIES).index
        sub = df[df[city_col].isin(top_cities)].copy()
        if not sub.empty:
            fig, ax = plt.subplots(figsize=(9, 4))
            sns.boxplot(data=sub, x=city_col, y='avg_salary_inr_pos', ax=ax)
            ax.set_yscale('log')
            ax.set_xlabel('City')
            ax.set_ylabel('Avg Salary (INR, log)')
            ax.set_title('Salary by City (Top)')
            plt.xticks(rotation=30, ha='right')
            savefig('salary_by_city.png')

    # 3) Top categories
    cat_col = 'category_searched_clean' if 'category_searched_clean' in df.columns else ('category_searched' if 'category_searched' in df.columns else None)
    if cat_col:
        vc = df[cat_col].value_counts().head(TOP_CATEGORIES)
        if not vc.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            vc.sort_values().plot(kind='barh', ax=ax)
            ax.set_title('Top Categories')
            ax.set_xlabel('Count')
            savefig('top_categories.png')

    # 4) Top companies
    comp_col = 'company_clean' if 'company_clean' in df.columns else ('company' if 'company' in df.columns else None)
    if comp_col:
        vc = df[comp_col].value_counts()
        # Exclude generic placeholders
        vc = vc[[i for i in vc.index if isinstance(i, str) and i.strip().lower() not in {'not specified', 'none', 'na', 'n/a'}]].head(TOP_COMPANIES)
        if not vc.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            vc.sort_values().plot(kind='barh', ax=ax)
            ax.set_title('Top Companies')
            ax.set_xlabel('Count')
            savefig('top_companies.png')

    # 5) Top skills
    skills_col = 'skills_clean' if 'skills_clean' in df.columns else ('skills' if 'skills' in df.columns else None)
    top_skills = []
    if skills_col:
        from collections import Counter
        counter = Counter()
        for s in df[skills_col].dropna():
            for sk in split_skills(s):
                counter[sk] += 1
        top_skills = [sk for sk, _ in counter.most_common(TOP_SKILLS)]
        if top_skills:
            ser = pd.Series({sk: counter[sk] for sk in top_skills})
            fig, ax = plt.subplots(figsize=(8, 5))
            ser.sort_values().plot(kind='barh', ax=ax)
            ax.set_title('Top Skills')
            ax.set_xlabel('Count')
            savefig('top_skills.png')

    # 6) Skill co-occurrence heatmap (top CO_SKILLS)
    if top_skills:
        co = top_skills[:CO_SKILLS]
        mat = pd.DataFrame(0, index=co, columns=co)
        for s in df[skills_col].dropna():
            lst = set(split_skills(s))
            present = [sk for sk in co if sk in lst]
            for i in range(len(present)):
                for j in range(len(present)):
                    if i != j:
                        mat.loc[present[i], present[j]] += 1
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(mat, cmap='Blues', ax=ax)
        ax.set_title('Skill Co-occurrence (Top)')
        savefig('skills_cooccurrence.png')

    # 7) Salary by experience level
    if 'experience_level' in df.columns and 'avg_salary_inr_pos' in df.columns:
        sub = df[['experience_level', 'avg_salary_inr_pos']].dropna()
        if not sub.empty:
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.boxplot(data=sub, x='experience_level', y='avg_salary_inr_pos', order=['Entry','Junior','Mid','Senior'], ax=ax)
            ax.set_yscale('log')
            ax.set_title('Salary by Experience Level')
            ax.set_xlabel('Experience Level')
            ax.set_ylabel('Avg Salary (INR, log)')
            savefig('salary_by_experience_level.png')

    # 8) Salary vs experience (scatter)
    if 'exp_min_years' in df.columns and 'avg_salary_inr_pos' in df.columns:
        sub = df[['exp_min_years', 'avg_salary_inr_pos']].dropna()
        if not sub.empty:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.scatterplot(data=sub, x='exp_min_years', y='avg_salary_inr_pos', alpha=0.4, ax=ax)
            ax.set_yscale('log')
            ax.set_xlabel('Min Experience (years)')
            ax.set_ylabel('Avg Salary (INR, log)')
            ax.set_title('Salary vs Experience')
            savefig('salary_vs_experience.png')

    # 9) City-category heatmap
    if city_col and cat_col:
        ct = pd.crosstab(df[city_col], df[cat_col])
        # Filter top cities/cats by totals
        ct = ct.loc[ct.sum(axis=1).sort_values(ascending=False).head(12).index]
        ct = ct[ct.sum(axis=0).sort_values(ascending=False).head(12).index]
        if not ct.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(ct, cmap='Greens', ax=ax)
            ax.set_title('City vs Category (Counts)')
            savefig('city_category_heatmap.png')

    # Append summary text to report
    lines = []
    lines.append("\n---\n")
    lines.append("## EDA Summary")

    # Text metrics (no dates/paths)
    lines.append(f"Rows analyzed: {len(df)}")
    nn_salary = int(df['avg_salary_inr'].notna().sum()) if 'avg_salary_inr' in df.columns else 0
    lines.append(f"Rows with salary: {nn_salary}")

    if city_col:
        city_counts = df[city_col].value_counts().head(5)
        lines.append("Top cities: " + ", ".join([f"{c} ({n})" for c, n in city_counts.items()]))

    if cat_col:
        cat_counts = df[cat_col].value_counts().head(5)
        lines.append("Top categories: " + ", ".join([f"{c} ({n})" for c, n in cat_counts.items()]))

    if comp_col:
        comp_counts = df[comp_col].value_counts().head(5)
        lines.append("Top companies: " + ", ".join([f"{c} ({n})" for c, n in comp_counts.items()]))

    if 'experience_level' in df.columns:
        lvl_counts = df['experience_level'].value_counts()
        items = [f"{lvl} ({lvl_counts.get(lvl, 0)})" for lvl in ['Entry','Junior','Mid','Senior'] if lvl in lvl_counts]
        if items:
            lines.append("Experience levels: " + ", ".join(items))

    # List created figures
    figs = [
        'salary_distribution.png',
        'salary_by_city.png',
        'top_categories.png',
        'top_companies.png',
        'top_skills.png',
        'skills_cooccurrence.png',
        'salary_by_experience_level.png',
        'salary_vs_experience.png',
        'city_category_heatmap.png'
    ]
    existing = [f for f in figs if os.path.exists(os.path.join(FIGDIR, f))]
    if existing:
        lines.append("Figures: " + ", ".join([os.path.join('reports','figures',f) for f in existing]))

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, 'a', encoding='utf-8') as f:
        f.write("\n" + "\n".join(lines))


if __name__ == '__main__':
    eda()
