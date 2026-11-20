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

---

## 3. Part B Model Card (`models/pipeline.joblib`)

- **Model & Task:** `GradientBoostingClassifier` inside a `scikit-learn` `Pipeline` (`ColumnTransformer` with median/most-frequent imputation, `StandardScaler`, and `OneHotEncoder`) predicting binary seat victory (`is_winner`: `1` = constituency winner, `0` = runner-up).
- **Split & Leakage Prevention:** Time-based split (`1970–2013` train: 15,826 rows; `2018–2024` test: 8,498 rows) performed before fitting any preprocessing transformer. Post-election variables (`Votes`, `log_votes`, `vote_share_pct`, `Turnout N`, `Rejected Votes`) and `Candidate Name` are strictly excluded to prevent target leakage.
- **Evaluation Results:** Selected over `DummyClassifier` (`CV PR-AUC: 0.1229`), `LogisticRegression` (`0.3693`), and `RandomForestClassifier` (`0.5832`) with `CV PR-AUC: 0.5958` and `CV ROC-AUC: 0.8903`. Held-out `2018–2024` test performance: `ROC-AUC = 0.8689`, `PR-AUC = 0.3939`, `F1 = 0.4476`.
- **Concrete Error Patterns & Limitations:**
  - **Party-Symbol / Coalition Shift (Concept Drift):** In 2024, PTI candidates contested as `IND (PTI)` (`PTI-IND`) rather than `PTI`, reducing recall on unseen party labels (`OneHotEncoder` maps unseen categories to all-zeros).
  - **Candidate-Level Blindness:** Because candidate names were anonymized (`"Unknown"`) in 2018 and excluded to prevent leakage, the model cannot capture individual candidate incumbency or local popularity.
- **Intended Use & Risks:** Intended strictly for educational analysis and historical competitiveness benchmarking. Must **not** be used for automated campaign resource allocation or voter persuasion without candidate-level polling and constituency delimitation updates.