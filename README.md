---
title: Pakistan Elections ML Pipeline
emoji: 🗳️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Pakistan Elections ML Pipeline: Pre-Election Seat Winner Classifier

A leakage-free tabular machine learning pipeline, REST API backend, and interactive web application for classifying Pakistan National Assembly seat winners and estimating pre-election win probabilities.

**Author:** Qudrat Ullah  
**Roll No (Trainee ID):** TRN-2026-000363  
**Date:** 2026-11-20  

---

## 1. Project Overview

Predicting election outcomes in Pakistan presents unique challenges due to multi-party fragmentation, candidate crowdedness, and regional political dynamics. This system implements an end-to-end pipeline that trains exclusively on **pre-election features** known before ballots are cast (avoiding target leakage from votes, vote shares, or turnout).

### Core Capabilities:
- **Leakage-Free Pre-Election Modeling:** Uses 7 strictly pre-election features (electoral roll size, candidate seat count, administrative province, macro-region, electoral zone, party, and political bloc).
- **Ensemble ML Pipeline:** `scikit-learn` `Pipeline` consisting of median/mode imputation, `StandardScaler`, `OneHotEncoder`, and `GradientBoostingClassifier` evaluated via Stratified 5-Fold Cross-Validation and held-out test splits.
- **FastAPI REST Service:** Production-ready backend with asynchronous lifespan model loading, Pydantic input validation, category metadata discovery, and batch CSV inference streaming.
- **Interactive Single-Page UI:** Zero-dependency modern frontend with preset scenarios, dynamic dropdowns, confidence gauges, and batch scoring tools.
- **Containerized Deployment:** Ready for local development, Hugging Face Spaces (Docker SDK), or Render (`port 7860`).

---

## 2. Model Feature Schema (7 Features)

| Feature | Type | Example | Description |
|---|---|---|---|
| `Registered Voters` | `float` | `380000.0` | Total registered voters in the constituency (`> 0`) |
| `num_candidates_in_seat` | `int` | `14` | Total contesting candidates in the seat (`1` to `100`) |
| `Province` | `str` | `"Punjab"` | Administrative province (`Punjab`, `Sindh`, `KPK`, `Balochistan`, `ICT`, `Unknown`) |
| `Regions 5` | `str` | `"All other Territories"` | Macro region (`All other Territories`, `KPK`, `Interior Sindh`, `Karachi`, `Balochistan`) |
| `Zones 20` | `str` | `"Zone-5 (Central -2) Lahore Division"` | Electoral zone string (21 unique administrative divisions) |
| `Party` | `str` | `"PML-N"` | Standardized political party abbreviation |
| `Six Parties` | `str` | `"PML (s)/IJI/PNA"` | Political party bloc or alliance |

---

## 3. Repository Structure

```text
pakistan-elections-ml-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml             # Continuous Integration pipeline
├── data/
│   ├── cleaned/
│   │   ├── elections.db       # SQLite relational database
│   │   └── elections_cleaned.csv # Cleaned training dataset (1970–2024)
│   └── raw/
│       └── pakistan-elections-database-1970-2024.csv
├── docs/
│   ├── assumptions.md         # Cleaning & modeling assumptions
│   ├── exploration.md         # Exploratory data analysis insights
│   └── schema.md              # Feature definitions & data types
├── frontend/
│   └── index.html             # Single-page interactive simulator UI
├── models/
│   └── pipeline.joblib        # Trained scikit-learn pipeline artifact
├── output/
│   ├── figures/               # Confusion matrix & distribution plots
│   └── reports/               # Model comparison & error analysis CSVs
├── sql/
│   └── queries.sql            # Analytical SQL queries
├── src/
│   ├── api.py                 # FastAPI backend application
│   ├── clean.py               # Data cleaning functions
│   ├── main.py                # Main workflow orchestration
│   ├── pipeline_part_a.py     # Part A ETL pipeline
│   ├── train_part_b.py        # Part B model training & evaluation
│   └── validate.py            # Data quality gate validators
├── tests/
│   ├── test_api.py            # FastAPI endpoint tests
│   └── test_cleaning.py       # Data cleaning unit tests
├── Dockerfile                 # Container specification (port 7860)
├── requirements.txt           # Pinned Python dependencies
└── README.md                  # Project documentation
```

---

## 4. Local Installation & Setup

### Prerequisites
- Python 3.12+ (tested on Python 3.12 and 3.14)
- Git

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/qudratullah-ai/pakistan-elections-ml-pipeline.git
cd pakistan-elections-ml-pipeline

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI Web Application
```bash
uvicorn src.api:app --reload --host 127.0.0.1 --port 8000
```

Open your browser and navigate to:
- **Interactive UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health Check:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 5. Docker Deployment

The application is containerized with `python:3.12-slim` and configured to listen on port `7860` (directly compatible with Hugging Face Spaces Docker SDK, Render, and AWS App Runner).

### Build Docker Image
```bash
docker build -t pakistan-elections-pipeline .
```

### Run Container Locally
```bash
docker run -p 7860:7860 pakistan-elections-pipeline
```

Access the application at [http://localhost:7860](http://localhost:7860).

---

## 6. API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the interactive HTML5/Vanilla JS frontend |
| `GET` | `/health` | Returns service health status and model readiness flag |
| `GET` | `/metadata` | Returns valid training categories for dropdown synchronization |
| `POST` | `/predict` | Predicts win status (1/0) and calibrated win probability percentage |
| `POST` | `/predict-batch` | Accepts a candidate CSV upload and streams back a scored CSV with predictions |

### Example `POST /predict` Request
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Registered Voters": 380000.0,
    "num_candidates_in_seat": 14,
    "Province": "Punjab",
    "Regions 5": "All other Territories",
    "Zones 20": "Zone-5 (Central -2) Lahore Division",
    "Party": "PML-N",
    "Six Parties": "PML (s)/IJI/PNA"
  }'
```

### Example `POST /predict` Response
```json
{
  "predicted_winner": 1,
  "label": "Likely Winner (1)",
  "win_probability": 78.45
}
```

---

## 7. Running Unit & Integration Tests

Run the full automated test suite (cleaning logic + API endpoints) using `pytest`:

```bash
python -m pytest -v
```

All tests should pass:
- `tests/test_cleaning.py` (7 tests for data quality and sanitization)
- `tests/test_api.py` (7 tests for health, UI, metadata, single prediction, validation, and batch CSV scoring)
