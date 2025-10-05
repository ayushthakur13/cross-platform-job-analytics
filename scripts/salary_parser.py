#!/usr/bin/env python3
"""
Salary parsing utilities for Cross Platform Job Analytics
- Handles LPA/lakh/lac formats
- Handles INR with monthly or yearly denominations (e.g., "₹ 50,000 /month", "₹6-8 LPA")
- Produces min, max, avg annual salary in INR
"""
from __future__ import annotations
import re
from typing import Optional, Tuple

LAKH_VALUE = 100_000  # 1 Lakh INR

_lpa_pattern = re.compile(
    r"(?P<min>\d+(?:\.\d+)?)\s*(?:-|to|–|—)?\s*(?P<max>\d+(?:\.\d+)?)?\s*(?:lpa|lac|lakh)s?",
    re.IGNORECASE,
)

_inr_pattern = re.compile(
    r"(?:\u20B9|rs\.?|inr)?\s*(?P<min>[\d,.]+)\s*(?:-|to|–|—)?\s*(?P<max>[\d,.]+)?\s*(?:/|per\s*)?(?P<period>month|yr|year|annum|pa|day|hour)?",
    re.IGNORECASE,
)

_single_lpa_pattern = re.compile(r"(?P<val>\d+(?:\.\d+)?)\s*(?:lpa|lac|lakh)s?", re.IGNORECASE)
_single_inr_pattern = re.compile(r"(?:\u20B9|rs\.?|inr)?\s*(?P<val>[\d,.]+)\s*(?:/|per\s*)?(?P<period>month|yr|year|annum|pa|day|hour)?", re.IGNORECASE)


def _to_number(val: str) -> Optional[float]:
    if val is None:
        return None
    try:
        return float(val.replace(",", ""))
    except Exception:
        return None


def _period_to_year_multiplier(period: Optional[str]) -> float:
    if not period:
        return 1.0  # assume already annual if unspecified
    p = period.lower()
    if p in {"yr", "year", "annum", "pa"}:
        return 1.0
    if p == "month":
        return 12.0
    if p == "day":
        return 365.0
    if p == "hour":
        # heuristic (8 hours * 22 days * 12 months)
        return 8 * 22 * 12
    return 1.0


def parse_salary_text(text: Optional[str]) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """
    Parse a salary string and return (min_annual_inr, max_annual_inr, avg_annual_inr)
    Returns (None, None, None) if parsing fails.
    """
    if not text or not isinstance(text, str):
        return (None, None, None)

    t = text.strip()
    if not t:
        return (None, None, None)

    # Try LPA ranges first
    m = _lpa_pattern.search(t)
    if m:
        min_val = _to_number(m.group("min"))
        max_val = _to_number(m.group("max")) or min_val
        if min_val is not None and max_val is not None:
            min_inr = int(round(min_val * LAKH_VALUE))
            max_inr = int(round(max_val * LAKH_VALUE))
            avg_inr = int(round((min_inr + max_inr) / 2))
            return (min_inr, max_inr, avg_inr)

    # Try INR ranges with period
    m = _inr_pattern.search(t)
    if m:
        min_val = _to_number(m.group("min"))
        max_val = _to_number(m.group("max")) or min_val
        period = m.group("period")
        mult = _period_to_year_multiplier(period)
        if min_val is not None and max_val is not None:
            min_inr = int(round(min_val * mult))
            max_inr = int(round(max_val * mult))
            avg_inr = int(round((min_inr + max_inr) / 2))
            return (min_inr, max_inr, avg_inr)

    # Single LPA value
    m = _single_lpa_pattern.search(t)
    if m:
        v = _to_number(m.group("val"))
        if v is not None:
            val_inr = int(round(v * LAKH_VALUE))
            return (val_inr, val_inr, val_inr)

    # Single INR value (assume annual if no period)
    m = _single_inr_pattern.search(t)
    if m:
        v = _to_number(m.group("val"))
        period = m.group("period")
        mult = _period_to_year_multiplier(period)
        if v is not None:
            val_inr = int(round(v * mult))
            return (val_inr, val_inr, val_inr)

    return (None, None, None)


if __name__ == "__main__":
    samples = [
        "₹ 50,000 /month",
        "₹40,000-60,000 /month",
        "6-8 LPA",
        "5 Lakh",
        "8.5 LPA",
        "₹ 8,00,000 /year",
        "Rs. 1,200 /day",
        "₹ 1000 /hour",
        None,
        "Not Disclosed",
    ]
    for s in samples:
        print(s, "->", parse_salary_text(s))
