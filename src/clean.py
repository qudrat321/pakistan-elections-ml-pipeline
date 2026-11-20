# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Data cleaning functions for the Pakistan Elections dataset (1970–2024)."""

import numpy as np
import pandas as pd

PARTY_MAPPING = {
    "muttahidda majlis-e-amal pakistan": "MMA",
    "mma": "MMA",
    "ji-p": "JI",
    "ji": "JI",
    "ind (pti)": "PTI-IND",
    "pakistan muslim league": "PML",
    "pml": "PML",
}


def strip_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Trim leading/trailing whitespace and collapse internal double spaces.

    Args:
        df: Input DataFrame.
        columns: List of string column names to clean.

    Returns:
        A new DataFrame with normalized whitespace and empty strings set to NaN.

    Raises:
        KeyError: If any column in `columns` does not exist in `df`.
    """
    out = df.copy()
    for col in columns:
        if col not in out.columns:
            raise KeyError(f"Column '{col}' not found in DataFrame.")
        out[col] = (
            out[col]
            .astype("string")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .replace("", pd.NA)
        )
    return out


def fix_numeric_types(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Coerce specified columns to numeric types, turning unparseable text into NaN.

    Args:
        df: Input DataFrame.
        columns: List of column names that should be numeric.

    Returns:
        A new DataFrame with numeric dtypes for `columns`.

    Raises:
        KeyError: If any column in `columns` does not exist in `df`.
    """
    out = df.copy()
    for col in columns:
        if col not in out.columns:
            raise KeyError(f"Column '{col}' not found in DataFrame.")
        if pd.api.types.is_string_dtype(out[col]):
            out[col] = out[col].str.replace(",", "", regex=False)
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def standardise_parties(df: pd.DataFrame, mapping: dict[str, str] = PARTY_MAPPING) -> pd.DataFrame:
    """Unify known political party spelling variants into canonical abbreviations.

    Args:
        df: Input DataFrame containing a 'Party' column.
        mapping: Dictionary mapping lowercase raw party names to canonical names.

    Returns:
        A new DataFrame with standardized values in 'Party'.

    Raises:
        KeyError: If 'Party' column is missing.
    """
    if "Party" not in df.columns:
        raise KeyError("Column 'Party' not found in DataFrame.")
    out = df.copy()
    lookup = {k.strip().lower(): v for k, v in mapping.items()}
    raw_clean = out["Party"].astype("string").str.strip()
    mapped = raw_clean.str.lower().map(lookup)
    out["Party"] = mapped.fillna(raw_clean)
    return out


def remove_exact_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove repeated candidate entries within the same Year and Constituency.

    Preserves candidates legitimately contesting multiple constituencies in the same
    year and distinct unnamed candidates, while removing partial-null row copies.

    Args:
        df: Input DataFrame.

    Returns:
        Tuple of (deduplicated DataFrame, count of removed rows).
    """
    out = df.drop_duplicates(keep="first").copy()
    if "Registered Voters" in out.columns:
        out = out.sort_values(by="Registered Voters", na_position="last")

    key_cols = ["Year", "Constituency", "Party", "Candidate Name", "Votes"]
    is_named = out["Candidate Name"].notna() & (~out["Candidate Name"].isin(["Unknown", "Unreadable"]))
    dup_mask = is_named & out.duplicated(subset=key_cols, keep="first")

    out = out[~dup_mask].sort_index().reset_index(drop=True)
    removed = len(df) - len(out)
    return out, removed


def handle_invalid_and_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Blank out physically impossible numeric values using vectorized NumPy rules.

    Args:
        df: Input DataFrame with numeric vote and voter columns.

    Returns:
        A new DataFrame with invalid numbers replaced by NaN.
    """
    out = df.copy()
    out["Votes"] = np.where(out["Votes"] < 0, np.nan, out["Votes"])
    out["Rejected Votes"] = np.where(out["Rejected Votes"] < 0, np.nan, out["Rejected Votes"])
    out["Registered Voters"] = np.where(out["Registered Voters"] <= 0, np.nan, out["Registered Voters"])
    out["Turnout N"] = np.where((out["Turnout N"] < 0) | (out["Turnout N"] > 100), np.nan, out["Turnout N"])
    out["Votes"] = np.where(out["Votes"] > out["Registered Voters"], np.nan, out["Votes"])
    return out


def handle_missing_values(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Propagate constituency-level metrics, fill categorical nulls, and drop rows missing Votes.

    Args:
        df: Input DataFrame.

    Returns:
        Tuple of (cleaned DataFrame, number of rows dropped).
    """
    out = df.copy()
    constituency_cols = ["Registered Voters", "Rejected Votes", "Turnout N"]
    for col in constituency_cols:
        out[col] = out.groupby(["Year", "Constituency"])[col].transform("first")

    cat_fill_cols = ["Province", "Party", "Candidate Name", "Regions 11", "Regions 5", "Six Parties"]
    for col in cat_fill_cols:
        if col in out.columns:
            out[col] = out[col].fillna("Unknown")

    before = len(out)
    out = out.dropna(subset=["Year", "Constituency", "Votes"]).reset_index(drop=True)
    dropped = before - len(out)
    return out, dropped