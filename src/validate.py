# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Validation checks and quality gate enforcement for cleaned election data."""

import pandas as pd


def check_not_null(df: pd.DataFrame, columns: list[str]) -> dict:
    """Verify that specified columns contain zero missing values.

    Args:
        df: DataFrame to validate.
        columns: Columns that must not contain NaN/null values.

    Returns:
        Dictionary with check name, passed count, total count, and pass_rate.

    Raises:
        KeyError: If any column in `columns` is missing from `df`.
    """
    for col in columns:
        if col not in df.columns:
            raise KeyError(f"Column '{col}' missing from DataFrame.")
    passed = int(df[columns].notna().all(axis=1).sum())
    total = len(df)
    rate = 1.0 if total == 0 else round(passed / total, 4)
    return {
        "check": f"not_null:{','.join(columns)}",
        "passed": passed,
        "total": total,
        "pass_rate": rate,
    }


def check_range(df: pd.DataFrame, column: str, min_val: float, max_val: float) -> dict:
    """Verify that all non-null values in `column` fall within [min_val, max_val].

    Args:
        df: DataFrame to validate.
        column: Numeric column to check.
        min_val: Minimum allowed value (inclusive).
        max_val: Maximum allowed value (inclusive).

    Returns:
        Dictionary with check name, passed count, total count, and pass_rate.

    Raises:
        KeyError: If `column` is missing from `df`.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' missing from DataFrame.")
    valid_series = df[column].dropna()
    passed = int(valid_series.between(min_val, max_val).sum())
    total = len(valid_series)
    rate = 1.0 if total == 0 else round(passed / total, 4)
    return {
        "check": f"range:{column}[{min_val},{max_val}]",
        "passed": passed,
        "total": total,
        "pass_rate": rate,
    }


def check_numeric_types(df: pd.DataFrame, columns: list[str]) -> dict:
    """Verify that all listed columns have numeric data types.

    Args:
        df: DataFrame to validate.
        columns: Columns expected to be numeric.

    Returns:
        Dictionary with check name, passed count, total count, and pass_rate.

    Raises:
        KeyError: If any column in `columns` is missing from `df`.
    """
    for col in columns:
        if col not in df.columns:
            raise KeyError(f"Column '{col}' missing from DataFrame.")
    passed = sum(pd.api.types.is_numeric_dtype(df[col]) for col in columns)
    total = len(columns)
    rate = 1.0 if total == 0 else round(passed / total, 4)
    return {
        "check": f"numeric_types:{','.join(columns)}",
        "passed": passed,
        "total": total,
        "pass_rate": rate,
    }


def check_unique_key(df: pd.DataFrame, subset: list[str]) -> dict:
    """Verify uniqueness across a composite key (excluding Unknown/Unreadable names).

    Args:
        df: DataFrame to validate.
        subset: List of columns forming the composite key.

    Returns:
        Dictionary with check name, passed count, total count, and pass_rate.

    Raises:
        KeyError: If any column in `subset` is missing from `df`.
    """
    for col in subset:
        if col not in df.columns:
            raise KeyError(f"Column '{col}' missing from DataFrame.")
    known_df = (
        df[~df["Candidate Name"].isin(["Unknown", "Unreadable"])]
        if "Candidate Name" in subset
        else df
    )
    passed = int((~known_df.duplicated(subset=subset)).sum())
    total = len(known_df)
    rate = 1.0 if total == 0 else round(passed / total, 4)
    return {
        "check": f"unique:{','.join(subset)}",
        "passed": passed,
        "total": total,
        "pass_rate": rate,
    }


def run_quality_gate(checks: list[dict], min_pass_rate: float = 0.99) -> float:
    """Compute overall validation pass rate and raise ValueError if below threshold.

    Args:
        checks: List of result dicts returned by check_* functions.
        min_pass_rate: Minimum acceptable overall pass rate (0.0 to 1.0).

    Returns:
        Overall pass rate as a float.

    Raises:
        ValueError: If overall pass rate is strictly less than `min_pass_rate`.
    """
    total_checked = sum(c["total"] for c in checks)
    total_passed = sum(c["passed"] for c in checks)
    overall = 1.0 if total_checked == 0 else round(total_passed / total_checked, 4)
    if overall < min_pass_rate:
        failing = [c["check"] for c in checks if c["pass_rate"] < min_pass_rate]
        raise ValueError(
            f"Quality Gate FAILED: pass rate {overall:.2%} < required {min_pass_rate:.2%}. "
            f"Failing checks: {failing}"
        )
    return overall
