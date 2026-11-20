# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""FastAPI Backend for Pakistan Elections Machine Learning Pipeline.

Provides interactive prediction endpoints, metadata discovery for UI dropdowns,
batch CSV scoring, and static frontend delivery.
"""

from contextlib import asynccontextmanager
import io
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from pydantic import BaseModel, ConfigDict, Field

# Base directories and resource paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent
MODEL_PATH: Path = BASE_DIR / "models" / "pipeline.joblib"
CLEANED_DATA_PATH: Path = BASE_DIR / "data" / "cleaned" / "elections_cleaned.csv"
FRONTEND_FILE: Path = BASE_DIR / "frontend" / "index.html"

# Model feature schema
REQUIRED_NUMERIC_FEATURES: List[str] = [
    "Registered Voters",
    "num_candidates_in_seat",
]
REQUIRED_CATEGORICAL_FEATURES: List[str] = [
    "Province",
    "Regions 5",
    "Zones 20",
    "Party",
    "Six Parties",
]
EXACT_FEATURE_COLUMNS: List[str] = (
    REQUIRED_NUMERIC_FEATURES + REQUIRED_CATEGORICAL_FEATURES
)

# Global model holder loaded during lifespan
model: Optional[Any] = None


def load_model_pipeline() -> Any:
    """Load model artifact into memory, raising clear RuntimeError if missing."""
    global model
    if model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(
                f"Trained model pipeline not found at '{MODEL_PATH}'. "
                "Please run 'python -m src.train_part_b' first to train and serialize the model."
            )
        model = joblib.load(MODEL_PATH)
    return model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to load the ML pipeline once at application startup."""
    load_model_pipeline()
    yield
    # Cleanup on shutdown if needed


app = FastAPI(
    title="Pakistan Elections ML Pipeline API",
    description=(
        "Production inference service for predicting National Assembly seat winners "
        "and win probabilities based on strictly pre-election features."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for browser integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CandidatePredictionInput(BaseModel):
    """Input payload validating the 7 pre-election features required by the classifier."""

    Registered_Voters: float = Field(
        ...,
        gt=0,
        alias="Registered Voters",
        description="Total registered voters in the constituency (must be > 0).",
        examples=[310000.0],
    )
    num_candidates_in_seat: int = Field(
        ...,
        ge=1,
        le=100,
        description="Total contesting candidates in the seat (must be between 1 and 100).",
        examples=[14],
    )
    Province: str = Field(
        ...,
        min_length=1,
        description="Administrative province (e.g. Punjab, Sindh, KPK, Balochistan, ICT, Unknown).",
        examples=["Punjab"],
    )
    Regions_5: str = Field(
        ...,
        min_length=1,
        alias="Regions 5",
        description="Macro geographic region (e.g. All other Territories, KPK, Interior Sindh, Karachi, Balochistan).",
        examples=["All other Territories"],
    )
    Zones_20: str = Field(
        ...,
        min_length=1,
        alias="Zones 20",
        description="Electoral administrative zone string.",
        examples=["Zone-5 (Central -2) Lahore Division"],
    )
    Party: str = Field(
        ...,
        min_length=1,
        description="Standardized political party abbreviation (e.g. PTI, PML-N, PPP, IND).",
        examples=["PML-N"],
    )
    Six_Parties: str = Field(
        ...,
        min_length=1,
        alias="Six Parties",
        description="Political party alliance/bloc categorization.",
        examples=["PML (s)/IJI/PNA"],
    )

    model_config = ConfigDict(populate_by_name=True)


class PredictionResponse(BaseModel):
    """Response schema containing the predicted outcome and calibrated probability."""

    predicted_winner: int = Field(
        ...,
        description="Binary outcome: 1 for projected winner, 0 for runner-up.",
        examples=[1],
    )
    label: str = Field(
        ...,
        description="Human-readable outcome description.",
        examples=["Likely Winner (1)"],
    )
    win_probability: float = Field(
        ...,
        description="Projected win probability percentage (0.0 to 100.0).",
        examples=[78.45],
    )


class MetadataResponse(BaseModel):
    """Metadata schema containing valid categories for user interface dropdowns."""

    provinces: List[str]
    regions_5: List[str]
    zones_20: List[str]
    parties: List[str]
    six_parties: List[str]
    Province: List[str]
    Regions_5: List[str] = Field(..., alias="Regions 5")
    Zones_20: List[str] = Field(..., alias="Zones 20")
    Party: List[str]
    Six_Parties: List[str] = Field(..., alias="Six Parties")
    hierarchy: Optional[Dict[str, Dict[str, List[str]]]] = None

    model_config = ConfigDict(populate_by_name=True)



def _get_fallback_metadata() -> Dict[str, List[str]]:
    """Return verified historical default categories if cleaned dataset is missing."""
    provinces = ["Balochistan", "ICT", "KPK", "Punjab", "Sindh", "Unknown"]
    regions_5 = [
        "All other Territories",
        "Balochistan",
        "Interior Sindh",
        "KPK",
        "Karachi",
    ]
    zones_20 = [
        "Zone-1 (North) Malakand Division",
        "Zone-1 (North) Rawalpindi Division",
        "Zone-1 (Quetta) Quetta, Zhob Divisions",
        "Zone-1 (West) Karachi Division",
        "Zone-2 (East) Mirpur Khas Division",
        "Zone-2 (South) Bannu, DIKhan, Kohat Divisions",
        "Zone-2 (West -1) Sargodha Division",
        "Zone-2 Kalat, Nasirabad,Sibi Divisions",
        "Zone-3 (Peshawar Valley) Peshawar & Mardan Divisions",
        "Zone-3 (South) Hyderabad Division",
        "Zone-3 (West -2) Faisalabad Division",
        "Zone-3 Makran Division",
        "Zone-4 (Central -1) Gujranwala Division",
        "Zone-4 (Hazara) Hazara Divison",
        "Zone-4 (North-1) Sukkur Division",
        "Zone-5 (Central -2) Lahore Division",
        "Zone-5 (North-2) Larkana Division",
        "Zone-6 (South -2) Multan Division",
        "Zone-7 (South -2) Dera Ghazi Khan Division",
        "Zone-8 (South -3) Bahawalpur Division",
        "Zone-new (Fata Tribal Area)",
    ]
    top_parties = [
        "IND",
        "PPP",
        "PML-N",
        "MQM",
        "PTI",
        "MMA",
        "JI",
        "TLP",
        "JUI-F",
        "ANP",
        "PML-Q",
        "BAP",
        "PML-F",
        "BNP",
        "MQM-P",
        "GDA",
        "PkMAP",
        "PTI-IND",
        "IPP",
        "NP",
        "PMAP",
        "JWP",
        "PPP-S",
        "PAT",
        "PSP",
    ]
    six_parties = [
        "Independent Parties",
        "Other Parties",
        "PML (s)/IJI/PNA",
        "PPP (s)/PDA",
        "PTI",
        "Province Parties",
        "Religious Parties",
        "Unknown",
    ]
    fallback_hierarchy = {
        "Balochistan": {
            "Balochistan": [
                "Zone-1 (Quetta) Quetta, Zhob Divisions",
                "Zone-2 Kalat, Nasirabad,Sibi Divisions",
                "Zone-3 Makran Division",
            ]
        },
        "ICT": {
            "All other Territories": ["Zone-1 (North) Rawalpindi Division"]
        },
        "KPK": {
            "KPK": [
                "Zone-1 (North) Malakand Division",
                "Zone-2 (South) Bannu, DIKhan, Kohat Divisions",
                "Zone-3 (Peshawar Valley) Peshawar & Mardan Divisions",
                "Zone-4 (Hazara) Hazara Divison",
                "Zone-new (Fata Tribal Area)",
            ]
        },
        "Punjab": {
            "All other Territories": [
                "Zone-1 (North) Rawalpindi Division",
                "Zone-2 (West -1) Sargodha Division",
                "Zone-3 (West -2) Faisalabad Division",
                "Zone-4 (Central -1) Gujranwala Division",
                "Zone-5 (Central -2) Lahore Division",
                "Zone-6 (South -2) Multan Division",
                "Zone-7 (South -2) Dera Ghazi Khan Division",
                "Zone-8 (South -3) Bahawalpur Division",
            ]
        },
        "Sindh": {
            "Interior Sindh": [
                "Zone-2 (East) Mirpur Khas Division",
                "Zone-3 (South) Hyderabad Division",
                "Zone-4 (North-1) Sukkur Division",
                "Zone-5 (North-2) Larkana Division",
            ],
            "Karachi": ["Zone-1 (West) Karachi Division"],
        },
        "Unknown": {
            "Balochistan": ["Zone-1 (Quetta) Quetta, Zhob Divisions"],
            "KPK": ["Zone-3 (Peshawar Valley) Peshawar & Mardan Divisions"],
        },
    }
    return {
        "provinces": sorted(provinces),
        "regions_5": sorted(regions_5),
        "zones_20": sorted(zones_20),
        "parties": top_parties,
        "six_parties": sorted(six_parties),
        "hierarchy": fallback_hierarchy,
    }



@app.get("/", response_class=HTMLResponse, summary="Serve Interactive Web Frontend")
def serve_index() -> HTMLResponse:
    """Serve the single-page interactive simulator application."""
    if not FRONTEND_FILE.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Frontend file not found at '{FRONTEND_FILE}'.",
        )
    html_content = FRONTEND_FILE.read_text(encoding="utf-8")
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@app.get("/health", summary="Health and Model Readiness Check")
def health_check() -> Dict[str, Any]:
    """Check API service health and confirm that the model pipeline is loaded."""
    current_model = model or (load_model_pipeline() if MODEL_PATH.exists() else None)
    return {
        "status": "ok",
        "model_loaded": current_model is not None,
    }


@app.get(
    "/metadata",
    response_model=MetadataResponse,
    summary="Get Training Category Lists for UI Dropdowns",
)
def get_metadata() -> Dict[str, Any]:
    """Extract sorted valid categories for dropdown synchronization."""
    if CLEANED_DATA_PATH.exists():
        try:
            df = pd.read_csv(CLEANED_DATA_PATH)
            provinces = sorted(df["Province"].dropna().unique().astype(str).tolist())
            regions_5 = sorted(df["Regions 5"].dropna().unique().astype(str).tolist())
            zones_20 = sorted(df["Zones 20"].dropna().unique().astype(str).tolist())
            six_parties = sorted(
                df["Six Parties"].dropna().unique().astype(str).tolist()
            )

            # Top 50 parties by historical frequency
            top_parties = (
                df["Party"]
                .dropna()
                .value_counts()
                .head(50)
                .index.astype(str)
                .tolist()
            )
            # Compute hierarchy mapping for cascading UI dropdowns
            hierarchy = {}
            for (prov, reg), sub in df.groupby(["Province", "Regions 5"]):
                prov_str = str(prov)
                reg_str = str(reg)
                zones = sorted(sub["Zones 20"].dropna().unique().astype(str).tolist())
                if prov_str not in hierarchy:
                    hierarchy[prov_str] = {}
                hierarchy[prov_str][reg_str] = zones

            data = {
                "provinces": provinces,
                "regions_5": regions_5,
                "zones_20": zones_20,
                "parties": top_parties,
                "six_parties": six_parties,
                "hierarchy": hierarchy,
            }

        except Exception:
            data = _get_fallback_metadata()
    else:
        data = _get_fallback_metadata()

    # Mirror both standardized names and dataset-identical field names
    data["Province"] = data["provinces"]
    data["Regions 5"] = data["regions_5"]
    data["Zones 20"] = data["zones_20"]
    data["Party"] = data["parties"]
    data["Six Parties"] = data["six_parties"]
    return data


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict Seat Outcome for a Single Candidate",
)
def predict_single(candidate: CandidatePredictionInput) -> PredictionResponse:
    """Predict candidate win outcome and calibrated percentage probability."""
    current_model = model or load_model_pipeline()
    if current_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded in server memory.",
        )

    # Build DataFrame matching exact feature column names
    row_dict = {
        "Registered Voters": float(candidate.Registered_Voters),
        "num_candidates_in_seat": int(candidate.num_candidates_in_seat),
        "Province": str(candidate.Province),
        "Regions 5": str(candidate.Regions_5),
        "Zones 20": str(candidate.Zones_20),
        "Party": str(candidate.Party),
        "Six Parties": str(candidate.Six_Parties),
    }
    input_df = pd.DataFrame([row_dict], columns=EXACT_FEATURE_COLUMNS)

    try:
        pred_arr = current_model.predict(input_df)
        pred_int = int(pred_arr[0])

        proba_arr = current_model.predict_proba(input_df)
        prob_float = float(proba_arr[0, 1])
        win_pct = round(prob_float * 100.0, 2)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference pipeline execution error: {str(exc)}",
        ) from exc

    label = "Likely Winner (1)" if pred_int == 1 else "Unlikely Winner (0)"

    return PredictionResponse(
        predicted_winner=pred_int,
        label=label,
        win_probability=win_pct,
    )


@app.post("/predict-batch", summary="Batch Inference from Uploaded CSV")
def predict_batch(file: UploadFile = File(...)) -> StreamingResponse:
    """Accept an uploaded CSV file, compute predictions, and stream back scored CSV."""
    current_model = model or load_model_pipeline()
    if current_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded in server memory.",
        )

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a valid .csv file.",
        )

    try:
        contents = file.file.read()
        df_upload = pd.read_csv(io.BytesIO(contents))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse uploaded CSV: {str(exc)}",
        ) from exc

    if df_upload.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded CSV file contains no data rows.",
        )

    # Normalize column names with case and punctuation variations
    normalized_mapping = {}
    for col in df_upload.columns:
        norm = col.strip().lower().replace("_", " ")
        if norm in ["registered voters", "registered voter"]:
            normalized_mapping[col] = "Registered Voters"
        elif norm in [
            "num candidates in seat",
            "num candidates",
            "candidates count",
            "candidate count",
        ]:
            normalized_mapping[col] = "num_candidates_in_seat"
        elif norm == "province":
            normalized_mapping[col] = "Province"
        elif norm in ["regions 5", "region 5", "regions5"]:
            normalized_mapping[col] = "Regions 5"
        elif norm in ["zones 20", "zone 20", "zones20"]:
            normalized_mapping[col] = "Zones 20"
        elif norm == "party":
            normalized_mapping[col] = "Party"
        elif norm in ["six parties", "six party", "sixparties"]:
            normalized_mapping[col] = "Six Parties"

    df_working = df_upload.rename(columns=normalized_mapping).copy()

    # Automatically derive 'num_candidates_in_seat' if missing but constituency info exists
    if "num_candidates_in_seat" not in df_working.columns:
        if "Year" in df_working.columns and "Constituency" in df_working.columns:
            df_working["num_candidates_in_seat"] = df_working.groupby(
                ["Year", "Constituency"]
            )["Party"].transform("count")
        elif "Constituency" in df_working.columns:
            df_working["num_candidates_in_seat"] = df_working.groupby("Constituency")[
                "Party"
            ].transform("count")
        else:
            # Fallback to total rows count or default 10
            df_working["num_candidates_in_seat"] = max(1, len(df_working))

    # Verify all 7 required feature columns exist
    missing_cols = [c for c in EXACT_FEATURE_COLUMNS if c not in df_working.columns]
    if missing_cols:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Missing required feature columns: {missing_cols}. "
                f"Required columns are: {EXACT_FEATURE_COLUMNS}"
            ),
        )

    try:
        X = df_working[EXACT_FEATURE_COLUMNS].copy()
        predictions = current_model.predict(X)
        probabilities = current_model.predict_proba(X)[:, 1]

        df_upload["predicted_winner"] = [int(p) for p in predictions]
        df_upload["win_probability"] = [
            round(float(p * 100.0), 2) for p in probabilities
        ]

        # Convert back to CSV buffer
        stream = io.StringIO()
        df_upload.to_csv(stream, index=False)
        csv_text = stream.getvalue()

        return Response(
            content=csv_text,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=predictions_{file.filename}"
            },
        )


    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction error: {str(exc)}",
        ) from exc
