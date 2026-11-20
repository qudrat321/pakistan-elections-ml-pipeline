# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Verification script: Starts Uvicorn server in a background thread and probes all endpoints."""

import json
import sys
import threading
import time
import urllib.request
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn
from src.api import app

PORT = 8008
HOST = "127.0.0.1"
BASE_URL = f"http://{HOST}:{PORT}"


def run_server():
    try:
        config = uvicorn.Config(
            app=app,
            host=HOST,
            port=PORT,
            log_level="warning",
        )
        server = uvicorn.Server(config)
        server.install_signal_handlers = lambda: None
        server.run()
    except Exception as e:
        print(f"Exception in run_server: {type(e).__name__}: {e}", flush=True)
        import traceback
        traceback.print_exc()





def main():
    print("Starting Uvicorn server thread...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Poll until server is ready (up to 15 seconds)
    started = False
    for attempt in range(30):
        try:
            with urllib.request.urlopen(f"{BASE_URL}/health", timeout=2) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    print(f"Server ready! Health: {data}")
                    started = True
                    break
        except Exception:
            time.sleep(0.5)

    if not started:
        print("ERROR: Server failed to start within timeout.")
        sys.exit(1)

    print("\n--- Testing 1: GET / ---")
    with urllib.request.urlopen(f"{BASE_URL}/") as resp:
        html = resp.read().decode("utf-8")
        print(f"Status: {resp.status}, Content length: {len(html)}")
        assert resp.status == 200
        assert "Pakistan Elections ML Classifier" in html
    print("PASS: GET /")

    print("\n--- Testing 2: GET /health ---")
    with urllib.request.urlopen(f"{BASE_URL}/health") as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"Status: {resp.status}, Payload: {data}")
        assert resp.status == 200
        assert data["status"] == "ok"
        assert data["model_loaded"] is True
    print("PASS: GET /health")

    print("\n--- Testing 3: GET /metadata ---")
    with urllib.request.urlopen(f"{BASE_URL}/metadata") as resp:
        meta = json.loads(resp.read().decode("utf-8"))
        print(f"Status: {resp.status}")
        print(f"Provinces ({len(meta['provinces'])}): {meta['provinces']}")
        print(f"Top 5 Parties: {meta['parties'][:5]}")
        assert resp.status == 200
        assert "Punjab" in meta["provinces"]
        assert "Six Parties" in meta
    print("PASS: GET /metadata")

    print("\n--- Testing 4: POST /predict ---")
    candidate_data = {
        "Registered Voters": 380000.0,
        "num_candidates_in_seat": 14,
        "Province": "Punjab",
        "Regions 5": "All other Territories",
        "Zones 20": "Zone-5 (Central -2) Lahore Division",
        "Party": "PML-N",
        "Six Parties": "PML (s)/IJI/PNA",
    }
    req = urllib.request.Request(
        f"{BASE_URL}/predict",
        data=json.dumps(candidate_data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        pred = json.loads(resp.read().decode("utf-8"))
        print(f"Status: {resp.status}, Prediction: {pred}")
        assert resp.status == 200
        assert "predicted_winner" in pred
        assert "label" in pred
        assert "win_probability" in pred
        assert pred["predicted_winner"] in [0, 1]
    print("PASS: POST /predict")

    print("\n--- Testing 5: POST /predict (Validation Error Check) ---")
    bad_data = {
        "Registered Voters": -50.0,  # Invalid: <= 0
        "num_candidates_in_seat": 150,  # Invalid: > 100
        "Province": "Punjab",
        "Regions 5": "All other Territories",
        "Zones 20": "Zone-5 (Central -2) Lahore Division",
        "Party": "PML-N",
        "Six Parties": "PML (s)/IJI/PNA",
    }
    req_bad = urllib.request.Request(
        f"{BASE_URL}/predict",
        data=json.dumps(bad_data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req_bad)
        assert False, "Expected HTTP 422 error"
    except urllib.error.HTTPError as err:
        print(f"Caught expected HTTP {err.code} validation error")
        assert err.code == 422
    print("PASS: POST /predict validation")

    print("\n--- Testing 6: POST /predict-batch (Multipart CSV Upload) ---")
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    csv_body = (
        "Registered Voters,num_candidates_in_seat,Province,Regions 5,Zones 20,Party,Six Parties\r\n"
        "350000,12,Punjab,All other Territories,Zone-5 (Central -2) Lahore Division,PML-N,PML (s)/IJI/PNA\r\n"
        "280000,22,KPK,KPK,Zone-3 (Peshawar Valley) Peshawar & Mardan Divisions,IND,Independent Parties\r\n"
    )
    multipart_data = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="candidates.csv"\r\n'
        f"Content-Type: text/csv\r\n\r\n"
        f"{csv_body}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    req_batch = urllib.request.Request(
        f"{BASE_URL}/predict-batch",
        data=multipart_data,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(multipart_data)),
        },
        method="POST",
    )
    with urllib.request.urlopen(req_batch) as resp:
        scored_csv = resp.read().decode("utf-8")
        print(f"Status: {resp.status}")
        print("Scored CSV header and rows:")
        print(scored_csv.strip())
        assert resp.status == 200
        assert "predicted_winner" in scored_csv
        assert "win_probability" in scored_csv
    print("PASS: POST /predict-batch")


    print("\n==============================================")
    print("ALL SERVER CHECKS PASSED: ENDPOINTS OPERATIONAL")
    print("==============================================")


if __name__ == "__main__":
    main()
