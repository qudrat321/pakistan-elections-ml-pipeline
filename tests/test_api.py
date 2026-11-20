# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Unit and integration tests for FastAPI backend inference service."""

import asyncio
import io
import sys
from pathlib import Path


import joblib
import pytest
from fastapi import HTTPException, UploadFile
from pydantic import ValidationError

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.api
from src.api import (
    CandidatePredictionInput,
    MODEL_PATH,
    get_metadata,
    health_check,
    predict_batch,
    predict_single,
    serve_index,
)


@pytest.fixture(autouse=True, scope="session")
def setup_model():
    """Ensure trained model is loaded into memory for API testing."""
    if src.api.model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(f"Trained model not found at {MODEL_PATH}")
        src.api.model = joblib.load(MODEL_PATH)


def test_health_check():
    """Verify health endpoint returns status ok and model readiness flag."""
    data = health_check()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True


def test_serve_frontend():
    """Verify the root endpoint serves the HTML frontend application."""
    response = serve_index()
    assert response.status_code == 200
    html_text = response.body.decode("utf-8")
    assert "Pakistan Elections ML Classifier" in html_text
    assert "Candidate Feature Simulator" in html_text


def test_get_metadata():
    """Verify metadata endpoint returns populated dropdown category lists."""
    data = get_metadata()
    for key in ["provinces", "regions_5", "zones_20", "parties", "six_parties"]:
        assert key in data
        assert isinstance(data[key], list)
        assert len(data[key]) > 0
    assert "Punjab" in data["provinces"]
    assert "PML-N" in data["parties"] or "PTI" in data["parties"]


def test_predict_single_success():
    """Verify single candidate prediction returns valid winner classification and probability."""
    payload = {
        "Registered Voters": 380000.0,
        "num_candidates_in_seat": 14,
        "Province": "Punjab",
        "Regions 5": "All other Territories",
        "Zones 20": "Zone-5 (Central -2) Lahore Division",
        "Party": "PML-N",
        "Six Parties": "PML (s)/IJI/PNA",
    }
    candidate = CandidatePredictionInput(**payload)
    result = predict_single(candidate)
    assert result.predicted_winner in [0, 1]
    assert "Winner" in result.label
    assert isinstance(result.win_probability, (int, float))
    assert 0.0 <= result.win_probability <= 100.0


def test_predict_single_validation_errors():
    """Verify Pydantic validation rejects negative voters or out-of-range candidate counts."""
    with pytest.raises(ValidationError):
        CandidatePredictionInput(
            **{
                "Registered Voters": -100.0,  # Invalid: <= 0
                "num_candidates_in_seat": 150,  # Invalid: > 100
                "Province": "Punjab",
                "Regions 5": "All other Territories",
                "Zones 20": "Zone-5 (Central -2) Lahore Division",
                "Party": "PML-N",
                "Six Parties": "PML (s)/IJI/PNA",
            }
        )


def test_predict_batch_csv_success():
    """Verify batch CSV prediction processes multi-candidate files and streams back scored CSV."""
    csv_bytes = (
        b"Registered Voters,num_candidates_in_seat,Province,Regions 5,Zones 20,Party,Six Parties\n"
        b"350000,12,Punjab,All other Territories,Zone-5 (Central -2) Lahore Division,PML-N,PML (s)/IJI/PNA\n"
        b"280000,22,KPK,KPK,Zone-3 (Peshawar Valley) Peshawar & Mardan Divisions,IND,Independent Parties\n"
    )
    upload_file = UploadFile(
        file=io.BytesIO(csv_bytes),
        size=len(csv_bytes),
        filename="test_candidates.csv",
        headers={"content-type": "text/csv"},
    )
    response = predict_batch(upload_file)
    assert response.media_type == "text/csv"
    assert "predictions_test_candidates.csv" in response.headers.get("content-disposition", "")
    body_content = response.body.decode("utf-8")
    assert "predicted_winner" in body_content
    assert "win_probability" in body_content
    assert "PML-N" in body_content





def test_predict_batch_missing_columns():
    """Verify batch CSV endpoint rejects CSV missing required features with HTTP 400."""
    bad_csv = b"Registered Voters,Province\n100000,Punjab\n"
    upload_file = UploadFile(
        file=io.BytesIO(bad_csv),
        size=len(bad_csv),
        filename="bad_candidates.csv",
        headers={"content-type": "text/csv"},
    )
    with pytest.raises(HTTPException) as exc_info:
        predict_batch(upload_file)
    assert exc_info.value.status_code == 400
    assert "Missing required feature columns" in exc_info.value.detail
