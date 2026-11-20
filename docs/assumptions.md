@'
# Assumptions, Limitations & Cleaning Decisions

## 1. Data-Cleaning Decisions & Justifications
- **UTF-8 BOM Stripping:** Raw CSV includes a byte-order mark (`\ufeff`) before `Year`. Loaded via `encoding="utf-8-sig"` so column headers match schema definitions.
- **Deduplication Key (`Year`, `Constituency`, `Party`, `Candidate Name`, `Votes`):**
  - Candidates in Pakistan can legitimately contest multiple constituencies in the same election year (`964` cases in raw data); including `Constituency` prevents deleting valid multi-seat candidacies.
  - All `3,353` rows in the `2018` election lack `Candidate Name` (`NaN`), and `12` rows in `NA-176` (`2024`) list `"Unreadable"`. Excluding `"Unknown"`/`"Unreadable"` names from duplicate removal avoids dropping distinct unnamed candidates.
  - `123` rows (`58` repeated candidate entries in `2024`) are partial-null row copies where one row has `Registered Voters` populated and the copy has `NaN`. Sorting non-null `Registered Voters` first keeps the complete record and drops the partial copy.
- **Structural Missingness Propagation:** `Registered Voters`, `Rejected Votes`, and `Turnout N` are recorded once per constituency (usually on the winner's row) rather than repeated across runner-ups (~88.6% missing at row level). We propagate constituency-level values via `groupby(["Year", "Constituency"]).transform("first")`.
- **Invalid Values & Outliers:** `Registered Voters <= 0` (`6` rows) and `Votes > Registered Voters` (`4` rows) are blanked to `NaN` rather than guessed. Rows missing core fields (`Year`, `Constituency`, `Votes`) are dropped (`193` rows).

## 2. What We Chose NOT to Fix (Limitations)
- **2018 Missing Candidate Names:** We replaced `NaN` with `"Unknown"` instead of scraping external ECP PDFs, keeping the pipeline self-contained and reproducible from the raw file.
- **Historical Constituency Delimitations:** Constituency boundaries and numbering (e.g., `NA-1` in 1970 vs. `NA-1` in 2024) changed across census delimitations; cross-year constituency comparisons reflect official seat codes as recorded.
- **Minor Regional Parties:** Standardized major spelling variants (`MMA`, `JI`, `PML`, `PTI-IND`), leaving smaller historical coalitions intact to avoid misclassifying distinct factions.
'@ | Set-Content -Path "docs\assumptions.md" -Encoding UTF8