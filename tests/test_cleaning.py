# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Unit tests for cleaning and validation functions."""

import numpy as np
import pandas as pd
import pytest

from src.clean import (
    fix_numeric_types,
    handle_invalid_and_outliers,
    handle_missing_values,
    remove_exact_duplicates,
    standardise_parties,
    strip_text_columns,
)
from src.validate import (
    check_not_null,
    check_numeric_types,
    check_range,
    check_unique_key,
    run_quality_gate,
)


def test_strip_text_columns():
    df = pd.DataFrame({"Party": ["  PML   N ", "   ", "PTI"]})
    res = strip_text_columns(df, ["Party"])
    assert res.loc[0, "Party"] == "PML N"
    assert pd.isna(res.loc[1, "Party"])


def test_fix_numeric_types():
    df = pd.DataFrame({"Votes": ["1,500", "invalid", "200"]})
    res = fix_numeric_types(df, ["Votes"])
    assert res.loc[0, "Votes"] == 1500.0
    assert pd.isna(res.loc[1, "Votes"])


def test_standardise_parties():
    df = pd.DataFrame({"Party": ["Muttahidda Majlis-e-Amal Pakistan", "JI-P", "PPP"]})
    res = standardise_parties(df)
    assert res["Party"].tolist() == ["MMA", "JI", "PPP"]


def test_remove_exact_duplicates():
    df = pd.DataFrame(
        {
            "Year": [2024, 2024, 2024],
            "Constituency": ["NA-1", "NA-1", "NA-2"],
            "Party": ["PTI", "PTI", "PTI"],
            "Candidate Name": ["Ali", "Ali", "Ali"],
            "Votes": [50000, 50000, 45000],
            "Registered Voters": [np.nan, 250000.0, 220000.0],
        }
    )
    res, removed = remove_exact_duplicates(df)
    assert removed == 1
    assert len(res) == 2
    assert res.loc[0, "Registered Voters"] == 250000.0


def test_handle_invalid_and_outliers():
    df = pd.DataFrame(
        {
            "Votes": [-10.0, 500.0, 200.0],
            "Rejected Votes": [5.0, -1.0, 10.0],
            "Registered Voters": [100.0, 100.0, 0.0],
            "Turnout N": [50.0, 125.0, 40.0],
        }
    )
    res = handle_invalid_and_outliers(df)
    assert pd.isna(res.loc[0, "Votes"])
    assert pd.isna(res.loc[1, "Votes"])
    assert pd.isna(res.loc[1, "Turnout N"])
    assert pd.isna(res.loc[2, "Registered Voters"])


def test_handle_missing_values():
    df = pd.DataFrame(
        {
            "Year": [2024, 2024, 2024],
            "Constituency": ["NA-1", "NA-1", "NA-2"],
            "Registered Voters": [250000.0, np.nan, 200000.0],
            "Rejected Votes": [3000.0, np.nan, 2000.0],
            "Turnout N": [48.5, np.nan, 50.0],
            "Province": [None, "KPK", "Punjab"],
            "Votes": [50000.0, 40000.0, np.nan],
        }
    )
    res, dropped = handle_missing_values(df)
    assert dropped == 1
    assert len(res) == 2
    assert res.loc[1, "Registered Voters"] == 250000.0
    assert res.loc[0, "Province"] == "Unknown"


def test_validation_and_quality_gate():
    df = pd.DataFrame(
        {
            "Year": [2024, 2024],
            "Candidate Name": ["Ali", "Sara"],
            "Votes": [100.0, 200.0],
            "Turnout N": [45.0, 150.0],
        }
    )
    checks = [
        check_not_null(df, ["Year", "Votes"]),
        check_numeric_types(df, ["Votes", "Turnout N"]),
        check_range(df, "Turnout N", 0, 100),
        check_unique_key(df, ["Year", "Candidate Name"]),
    ]
    with pytest.raises(ValueError):
        run_quality_gate(checks, min_pass_rate=0.95)
