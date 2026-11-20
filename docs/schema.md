# Raw Dataset Schema (`pakistan-elections-database-1970-2024.csv`)

- **Dimensions:** 24,585 rows × 17 columns (11 general elections: 1970–2024)
- **Encoding:** UTF-8 with BOM (`utf-8-sig` required to strip `\ufeff` from `Year`)

| Column Name | Raw Dtype | Meaning & Units | Allowed Values / Range | Missing Count (%) |
| :--- | :--- | :--- | :--- | :--- |
| `Year` | `int64` | Election year (calendar year) | `{1970, 1977, 1988, 1990, 1993, 1997, 2002, 2008, 2013, 2018, 2024}` | 0 (0.00%) |
| `Constituency` | `object` | Full seat code & name (e.g., `NA-1 - Peshawar`) | Non-empty string | 0 (0.00%) |
| `NA` | `object` | National Assembly seat code (e.g., `NA-1`) | Non-empty string (`NA-*`) | 0 (0.00%) |
| `Province` | `object` | Administrative province/territory | `Punjab`, `Sindh`, `KPK`, `Balochistan`, `ICT` | 34 (0.14%) |
| `District` | `object` | Administrative district | Non-empty string | 0 (0.00%) |
| `Division` | `object` | Administrative division | Non-empty string | 0 (0.00%) |
| `Party` | `object` | Political party abbreviation or `IND` | 475 raw strings (requires standardization) | 2 (0.01%) |
| `Candidate Name` | `object` | Name of contesting candidate | String (missing across all 2018 records) | 3,354 (13.64%) |
| `Regions 11` | `object` | 11-region geographic grouping | Non-empty string | 1 (0.00%) |
| `Regions 12` | `object` | 12-region geographic grouping | Non-empty string | 0 (0.00%) |
| `Regions 5` | `object` | 5-region macro grouping | `All other Territories`, `KPK`, `Interior Sindh`, `Karachi`, `Balochistan` | 1 (0.00%) |
| `Registered Voters` | `float64` | Total registered voters in constituency (count) | Integer `> 0` (recorded once per constituency) | 21,780 (88.59%) |
| `Rejected Votes` | `float64` | Invalid ballots cast in constituency (count) | Integer `>= 0` (recorded once per constituency) | 21,954 (89.30%) |
| `Six Parties` | `object` | Political bloc grouping (7 categories) | e.g., `Independent Parties`, `PPP (s)/PDA`, `PTI` | 40 (0.16%) |
| `Turnout N` | `float64` | Constituency voter turnout percentage (`%`) | `0.0` to `100.0` | 21,958 (89.31%) |
| `Zones 20` | `object` | 20-zone electoral classification | Non-empty string | 0 (0.00%) |
| `Votes` | `float64` | Valid votes received by candidate (count) | Integer `>= 0` | 193 (0.79%) |