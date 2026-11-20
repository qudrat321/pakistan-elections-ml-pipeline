# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""End-to-end Part A pipeline: load, clean, validate, analyze, chart, and export SQLite."""

import json
import sqlite3
import sys
from pathlib import Path

import matplotlib

matplotlib.use(
    "Agg"
)  # Non-interactive backend so script runs cleanly in headless/CI environments
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW = (
    PROJECT_ROOT / "data" / "raw" / "pakistan-elections-database-1970-2024.csv"
)
CLEANED_CSV = PROJECT_ROOT / "data" / "cleaned" / "elections_cleaned.csv"
SQLITE_DB = PROJECT_ROOT / "data" / "cleaned" / "elections.db"
SQL_FILE = PROJECT_ROOT / "sql" / "queries.sql"
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"
REPORTS_DIR = PROJECT_ROOT / "output" / "reports"

NUMERIC_COLS = ["Year", "Registered Voters", "Rejected Votes", "Turnout N", "Votes"]
TEXT_COLS = [
    "Constituency",
    "NA",
    "Province",
    "District",
    "Division",
    "Party",
    "Candidate Name",
    "Regions 11",
    "Regions 12",
    "Regions 5",
    "Six Parties",
    "Zones 20",
]


def generate_visualizations(df: pd.DataFrame, figures_dir: Path) -> list[str]:
    """Generate and save three election analysis charts with titles and unit-labeled axes.

    Args:
        df: Cleaned elections DataFrame.
        figures_dir: Directory where PNG figures will be saved.

    Returns:
        List of saved figure filenames.
    """
    figures_dir.mkdir(parents=True, exist_ok=True)
    saved_files = []

    # Chart 1: Average Constituency Voter Turnout by Election Year (Line Chart)
    constituency_turnout = (
        df.groupby(["Year", "Constituency"], as_index=False)["Turnout N"]
        .first()
        .groupby("Year", as_index=False)["Turnout N"]
        .mean()
        .dropna()
    )
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.plot(
        constituency_turnout["Year"],
        constituency_turnout["Turnout N"],
        marker="o",
        linewidth=2,
        color="#1f77b4",
    )
    ax.set_title(
        "Average Constituency Voter Turnout in Pakistan General Elections (1970–2024)"
    )
    ax.set_xlabel("Election Year (Calendar Year)")
    ax.set_ylabel("Mean Voter Turnout (%)")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    f1 = "01_turnout_by_year.png"
    fig.savefig(figures_dir / f1, dpi=150)
    plt.close(fig)
    saved_files.append(f1)

    # Chart 2: Top 10 Parties by Total Votes in 2024 (Horizontal Bar Chart)
    df_2024 = df[df["Year"] == 2024]
    top_parties_2024 = (
        df_2024.groupby("Party", as_index=False)["Votes"]
        .sum()
        .sort_values("Votes", ascending=False)
        .head(10)
        .sort_values("Votes", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(top_parties_2024["Party"], top_parties_2024["Votes"] / 1e6, color="#2ca02c")
    ax.set_title(
        "Top 10 Political Parties / Blocs by Total Valid Votes (2024 Election)"
    )
    ax.set_xlabel("Total Valid Votes (Millions of Votes)")
    ax.set_ylabel("Political Party / Affiliation")
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    fig.tight_layout()
    f2 = "02_top_parties_2024_votes.png"
    fig.savefig(figures_dir / f2, dpi=150)
    plt.close(fig)
    saved_files.append(f2)

    # Chart 3: Distribution of Log-Transformed Candidate Votes Across All Elections (Histogram)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.hist(df["log_votes"], bins=40, color="#ff7f0e", edgecolor="black", alpha=0.85)
    ax.set_title("Distribution of Candidate Vote Counts (Log1p Scale, 1970–2024)")
    ax.set_xlabel("Log-Transformed Votes [log(1 + Votes)]")
    ax.set_ylabel("Number of Candidate Entries (Count)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    f3 = "03_log_votes_distribution.png"
    fig.savefig(figures_dir / f3, dpi=150)
    plt.close(fig)
    saved_files.append(f3)

    return saved_files


def run_part_a(raw_path: Path = DEFAULT_RAW, min_pass_rate: float = 0.99) -> dict:
    """Execute the complete Part A reproducible data pipeline and save all outputs.

    Args:
        raw_path: Path to input raw CSV file.
        min_pass_rate: Minimum overall validation pass rate required by quality gate.

    Returns:
        Dictionary of data-quality metrics and summary findings.
    """
    CLEANED_CSV.parent.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load Raw Data (Read-Only)
    raw_path = Path(raw_path)
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at: {raw_path}")
    df_raw = pd.read_csv(raw_path, encoding="utf-8-sig", low_memory=False)
    missing_pct_before = round(float(df_raw.isna().mean().mean() * 100), 2)

    # 2. Clean Data Step-by-Step
    df = strip_text_columns(df_raw, TEXT_COLS)
    df = fix_numeric_types(df, NUMERIC_COLS)
    df = standardise_parties(df)
    df, duplicates_removed = remove_exact_duplicates(df)
    df = handle_invalid_and_outliers(df)
    df, rows_dropped = handle_missing_values(df)

    # 3. Vectorized NumPy Feature Engineering (at least 2 vectorized ops required)
    df["log_votes"] = np.log1p(df["Votes"].to_numpy())
    df["vote_share_pct"] = np.where(
        df["Registered Voters"].notna() & (df["Registered Voters"] > 0),
        np.round((df["Votes"] / df["Registered Voters"]) * 100, 2),
        np.nan,
    )
    # Derive winner flag per (Year, Constituency) for downstream analysis and Part B ML
    max_seat_votes = df.groupby(["Year", "Constituency"])["Votes"].transform("max")
    df["is_winner"] = np.where(
        (df["Votes"] == max_seat_votes) & (df["Votes"] > 0), 1, 0
    )

    # 4. Validate Cleaned Data & Enforce Quality Gate (+2 Bonus)
    checks = [
        check_not_null(df, ["Year", "Constituency", "Party", "Province", "Votes"]),
        check_numeric_types(df, NUMERIC_COLS + ["log_votes"]),
        check_range(df, "Year", 1970, 2024),
        check_range(df, "Turnout N", 0.0, 100.0),
        check_range(df, "Votes", 0.0, 1e7),
        check_unique_key(
            df, ["Year", "Constituency", "Party", "Candidate Name", "Votes"]
        ),
    ]
    overall_pass_rate = run_quality_gate(checks, min_pass_rate=min_pass_rate)

    # 5. Save Cleaned CSV
    df.to_csv(CLEANED_CSV, index=False)
    missing_pct_after = round(float(df.isna().mean().mean() * 100), 2)

    # 6. Pandas Grouping & Pivot Summaries
    province_pivot = pd.pivot_table(
        df,
        values="Votes",
        index="Province",
        columns="Year",
        aggfunc="sum",
        fill_value=0,
    )
    province_pivot.to_csv(REPORTS_DIR / "votes_by_province_year_pivot.csv")

    # 7. SQLite Database Export & Analytical Query
    with sqlite3.connect(SQLITE_DB) as conn:
        df.to_sql("elections", conn, if_exists="replace", index=False)
        sql_query = SQL_FILE.read_text(encoding="utf-8")
        sql_results = pd.read_sql_query(sql_query, conn)
        sql_results.to_csv(REPORTS_DIR / "sql_top_parties.csv", index=False)

    # 8. Generate 3 Visualizations
    saved_charts = generate_visualizations(df, FIGURES_DIR)

    # 9. Write Data Quality Metrics Report (metrics.json)
    metrics = {
        "raw_rows": int(len(df_raw)),
        "cleaned_rows": int(len(df)),
        "duplicates_removed": int(duplicates_removed),
        "rows_dropped_missing_core": int(rows_dropped),
        "missing_cells_pct_before": missing_pct_before,
        "missing_cells_pct_after": missing_pct_after,
        "overall_validation_pass_rate": overall_pass_rate,
        "validation_checks": checks,
        "generated_charts": saved_charts,
    }
    with open(REPORTS_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Part A Pipeline succeeded!")
    print(f"Cleaned rows: {len(df):,} | Pass rate: {overall_pass_rate:.2%}")
    return metrics


if __name__ == "__main__":
    input_csv = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RAW
    run_part_a(raw_path=input_csv)
