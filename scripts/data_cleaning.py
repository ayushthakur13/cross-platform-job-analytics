#!/usr/bin/env python3
"""
Data Cleaning Pipeline for Cross Platform Job Analytics (Phase 2)
- Loads raw dataset
- Cleans/standardizes key fields
- Parses salary and experience
- Standardizes dates
- Creates derived features
- Saves cleaned dataset and appends summary to report
"""
from __future__ import annotations
import argparse
import os
from datetime import datetime, timedelta
import re
import pandas as pd

from salary_parser import parse_salary_text

DEFAULT_INPUT = os.path.join('data', 'raw', 'unified_jobs_dataset.csv')
DEFAULT_OUTPUT = os.path.join('data', 'processed', 'cleaned_jobs_dataset.csv')
DEFAULT_REPORT = os.path.join('reports', 'data_cleaning_report.md')

TIER1 = {"Delhi", "Bangalore", "Mumbai", "Pune", "Hyderabad", "Chennai", "Gurgaon", "Noida"}


def parse_experience(text: str):
    if not isinstance(text, str) or not text.strip():
        return (None, None)
    t = text.lower().strip()
    # Range like 2-4 years or 1 to 3 yrs
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:to|-|–|—)\s*(\d+(?:\.\d+)?)\s*(?:year|yr)s?", t)
    if m:
        return (float(m.group(1)), float(m.group(2)))
    # Single like 3+ years or 3 years
    m = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:year|yr)s?", t)
    if m:
        v = float(m.group(1))
        return (v, v)
    # Fresher
    if re.search(r"fresher|0\s*(?:year|yr)s?", t):
        return (0.0, 0.0)
    return (None, None)


def experience_level(min_years, max_years):
    if min_years is None and max_years is None:
        return None
    v = max(filter(lambda x: x is not None, [min_years, max_years])) if any([min_years, max_years]) else None
    if v is None:
        return None
    if v < 1:
        return 'Entry'
    if v < 3:
        return 'Junior'
    if v < 6:
        return 'Mid'
    return 'Senior'


def parse_posting_date(text: str, ref_date: datetime):
    if not isinstance(text, str) or not text.strip():
        return None
    t = text.lower().strip()
    # e.g., '2 days ago', '3 weeks ago', '1 month ago', 'today', 'yesterday'
    if 'today' in t:
        return ref_date.date()
    if 'yesterday' in t:
        return (ref_date - timedelta(days=1)).date()
    m = re.search(r"(\d+)\s*(day|week|month)s?\s*ago", t)
    if m:
        n = int(m.group(1))
        unit = m.group(2)
        if unit == 'day':
            return (ref_date - timedelta(days=n)).date()
        if unit == 'week':
            return (ref_date - timedelta(weeks=n)).date()
        if unit == 'month':
            # approximate as 30 days per month
            return (ref_date - timedelta(days=30*n)).date()
    # Fallback: try datetime parsing
    try:
        return pd.to_datetime(text, errors='coerce').date()
    except Exception:
        return None


def normalize_skills(s: str):
    if not isinstance(s, str) or not s.strip():
        return None
    parts = [p.strip() for p in s.split(',') if p.strip()]
    # De-duplicate while preserving order
    seen = set()
    cleaned = []
    for p in parts:
        key = p.lower()
        if key not in seen:
            seen.add(key)
            # Title-case for presentation; keep common acronyms upper-case
            val = p.title()
            for acro in ['ML', 'DL', 'NLP', 'AI', 'SQL', 'CSS', 'HTML', 'AWS', 'GCP']:
                val = re.sub(rf"\b{acro.title()}\b", acro, val)
            cleaned.append(val)
    return ', '.join(cleaned) if cleaned else None


def location_tier(city: str):
    if not isinstance(city, str) or not city.strip():
        return None
    c = city.strip().title()
    return 'Tier 1' if c in TIER1 else 'Tier 2/3'


def clean_text(x: str):
    return x.strip() if isinstance(x, str) else x

# Company normalization: strip legal suffixes and collapse spaces
LEGAL_SUFFIXES = [
    ' private limited', ' pvt ltd', ' pvt. ltd.', ' ltd', ' limited', ' llp', ' inc', ' corp', ' corporation', ' co.', ' co', ' plc', ' gmbh'
]

def normalize_company(name: str):
    if not isinstance(name, str):
        return name
    n = name.strip()
    n_low = n.lower()
    # remove legal suffixes
    changed = True
    while changed:
        changed = False
        for s in LEGAL_SUFFIXES:
            if n_low.endswith(s):
                n_low = n_low[: -len(s)]
                changed = True
    n = n_low.title().strip()
    # collapse multiple spaces
    n = re.sub(r"\s+", " ", n)
    return n if n else None

# City normalization mapping
CITY_MAP = {
    'bengaluru': 'Bangalore', 'bangaluru': 'Bangalore', 'delhi/ncr': 'Delhi', 'gurugram': 'Gurgaon',
    'bombay': 'Mumbai', 'cochin': 'Kochi', 'trivandrum': 'Thiruvananthapuram', 'tvm': 'Thiruvananthapuram'
}

def normalize_city(city: str):
    if not isinstance(city, str):
        return city
    c = city.strip()
    c_low = c.lower()
    c_std = CITY_MAP.get(c_low, c.title())
    return c_std

# Job type normalization
JOBTYPE_MAP = {
    'full time': 'Full-time', 'full-time': 'Full-time', 'part time': 'Part-time', 'part-time': 'Part-time',
    'internship': 'Internship', 'contract': 'Contract', 'freelance': 'Freelance', 'remote': 'Remote'
}

def normalize_job_type(v: str):
    if not isinstance(v, str):
        return v
    t = v.strip().lower()
    return JOBTYPE_MAP.get(t, v.title())

# Category normalization (lightweight)
CATEGORY_MAP = {
    'angular.js development': 'Angular Development',
    'node.js development': 'Node.js Development',
    'javascript development': 'JavaScript Development',
    'ai': 'Artificial Intelligence (AI)'
}

def normalize_category(cat: str):
    if not isinstance(cat, str):
        return cat
    c = cat.strip()
    c_low = c.lower()
    return CATEGORY_MAP.get(c_low, c)

# Skill synonyms
SKILL_MAP = {
    'ml': 'Machine Learning',
    'ai': 'Artificial Intelligence',
    'js': 'JavaScript',
    'node': 'Node.js',
    'golang': 'Go',
}

def normalize_skill_token(token: str):
    if not isinstance(token, str):
        return token
    t = token.strip()
    repl = SKILL_MAP.get(t.lower())
    return (repl or t).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=DEFAULT_INPUT)
    parser.add_argument('--output', default=DEFAULT_OUTPUT)
    parser.add_argument('--report', default=DEFAULT_REPORT)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(os.path.dirname(args.report), exist_ok=True)

    print(f"Loading dataset: {args.input}")
    df = pd.read_csv(args.input)
    original_rows = len(df)

    # Drop exact duplicate rows
    df = df.drop_duplicates()

    # Drop dup by job_url else by (title, company)
    if 'job_url' in df.columns:
        df = df.drop_duplicates(subset=['job_url'])
    elif all(c in df.columns for c in ['title', 'company']):
        df = df.drop_duplicates(subset=['title', 'company'])

    # Normalize obvious placeholder tokens to missing
    placeholder_tokens = {"not specified", "n/a", "na", "none", "null", "-", "—", "not disclosed"}
    def normalize_missing(x):
        if isinstance(x, str) and x.strip().lower() in placeholder_tokens:
            return None
        return x
    for col in ['title', 'company', 'city', 'category_searched', 'salary_text', 'skills', 'experience_text', 'job_type', 'posting_date_text']:
        if col in df.columns:
            df[col] = df[col].apply(normalize_missing)

    # Clean text fields
    for col in ['title', 'company', 'city', 'category_searched']:
        if col in df.columns:
            df[col + '_clean'] = df[col].apply(clean_text)

    # Company normalization
    if 'company_clean' in df.columns:
        df['company_norm'] = df['company_clean'].apply(normalize_company)

    # City normalization mapping
    if 'city_clean' in df.columns:
        df['city_clean'] = df['city_clean'].apply(lambda x: x.title() if isinstance(x, str) else x)
        df['city_norm'] = df['city_clean'].apply(normalize_city)

    # Category normalization
    if 'category_searched_clean' in df.columns:
        df['category_standard'] = df['category_searched_clean'].apply(normalize_category)

    # Skills normalization
    if 'skills' in df.columns:
        df['skills_clean'] = df['skills'].apply(normalize_skills)
        # Map skill tokens via synonyms
        def map_skills(s):
            if not isinstance(s, str):
                return s
            items = [normalize_skill_token(p.strip()) for p in s.split(',') if p.strip()]
            # dedupe preserving order
            seen = set(); out = []
            for it in items:
                low = it.lower()
                if low not in seen:
                    seen.add(low); out.append(it)
            return ', '.join(out) if out else None
        df['skills_clean'] = df['skills_clean'].apply(map_skills)

    # Salary parsing
    if 'salary_text' in df.columns:
        parsed = df['salary_text'].apply(parse_salary_text)
        df['min_salary_inr'] = parsed.apply(lambda x: x[0])
        df['max_salary_inr'] = parsed.apply(lambda x: x[1])
        df['avg_salary_inr'] = parsed.apply(lambda x: x[2])

    # Experience parsing (with months support)
    def parse_experience_with_months(text: str):
        if not isinstance(text, str) or not text.strip():
            return (None, None)
        t = text.lower().strip()
        # months range
        m = re.search(r"(\d+)\s*(?:to|-|–|—)\s*(\d+)\s*month", t)
        if m:
            a = float(m.group(1))/12.0; b = float(m.group(2))/12.0
            return (a, b)
        # single months
        m = re.search(r"(\d+)\s*month", t)
        if m:
            v = float(m.group(1))/12.0
            return (v, v)
        return parse_experience(text)

    if 'experience_text' in df.columns:
        exp_parsed = df['experience_text'].apply(parse_experience_with_months)
        df['exp_min_years'] = exp_parsed.apply(lambda x: x[0])
        df['exp_max_years'] = exp_parsed.apply(lambda x: x[1])
        df['experience_level'] = df.apply(lambda r: experience_level(r.get('exp_min_years'), r.get('exp_max_years')), axis=1)

    # Posting date standardization
    ref_dt = datetime.now()
    if 'posting_date_text' in df.columns:
        df['posting_date'] = df['posting_date_text'].apply(lambda x: parse_posting_date(x, ref_dt))

    # Job type normalization and flags
    if 'job_type' in df.columns:
        df['job_type'] = df['job_type'].apply(normalize_job_type)
        df['is_internship'] = df['job_type'].fillna('').str.contains('Internship', case=False)

    # Location tier
    base_city_col = 'city_norm' if 'city_norm' in df.columns else ('city_clean' if 'city_clean' in df.columns else ('city' if 'city' in df.columns else None))
    if base_city_col:
        df['location_tier'] = df[base_city_col].apply(location_tier)

    # Salary LPA and capped values for robust analytics
    if 'avg_salary_inr' in df.columns:
        df['avg_salary_lpa'] = df['avg_salary_inr'].apply(lambda v: v/100000 if pd.notna(v) else v)
        pos = df['avg_salary_inr'].dropna()
        pos = pos[pos > 0]
        if not pos.empty:
            lo = pos.quantile(0.01)
            hi = pos.quantile(0.99)
            df['avg_salary_inr_capped'] = df['avg_salary_inr'].clip(lower=lo, upper=hi)
            df['avg_salary_lpa_capped'] = df['avg_salary_inr_capped']/100000.0

    # Remote flag from location_full/city
    def detect_remote(row):
        for col in ['location_full', base_city_col]:
            if col in df.columns:
                v = row.get(col)
                if isinstance(v, str) and ('remote' in v.lower() or 'work from home' in v.lower()):
                    return True
        return False
    df['has_remote'] = df.apply(detect_remote, axis=1)

    # Enhanced deduplication after normalization
    dedup_subset = [c for c in ['title_clean','company_norm','city_norm'] if c in df.columns]
    if dedup_subset:
        df = df.drop_duplicates(subset=dedup_subset)

    # Data quality flags
    for col in ['salary_text', 'skills', 'experience_text', 'description']:
        if col in df.columns:
            df[f'has_{col}'] = df[col].notna()

    # Save cleaned dataset
    df.to_csv(args.output, index=False)
    print(f"Saved cleaned dataset: {args.output} ({len(df)} rows, from {original_rows} original)")

    # Append summary to report
    lines = []
    lines.append("\n---\n")
    lines.append("## Cleaning Summary")
    lines.append(f"Rows: {len(df)} (from {original_rows})")

    for col in ['min_salary_inr', 'max_salary_inr', 'avg_salary_inr', 'exp_min_years', 'exp_max_years', 'experience_level', 'posting_date', 'location_tier']:
        if col in df.columns:
            non_null = df[col].notna().sum()
            lines.append(f"- Non-null {col}: {non_null} ({non_null/len(df)*100:.1f}%)")

    with open(args.report, 'a', encoding='utf-8') as f:
        f.write("\n".join(lines))


if __name__ == '__main__':
    main()
