# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Generates an ultra-detailed, professional system architecture diagram for the Pakistan Elections ML Pipeline."""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_IMG = FIGURES_DIR / "05_system_architecture.png"

def create_architecture_diagram():
    # High resolution canvas (18 x 11.5 inches at 150 DPI = 2700 x 1725 px)
    fig, ax = plt.subplots(figsize=(18, 11.5), dpi=150)
    fig.patch.set_facecolor('#0B1120')  # Deep modern dark navy background
    ax.set_facecolor('#0B1120')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header Title Banner
    ax.text(50, 96.5, "PAKISTAN ELECTIONS ML PIPELINE - COMPLETE SYSTEM ARCHITECTURE",
            ha='center', va='center', fontsize=21, fontweight='bold', color='#F8FAFC', fontfamily='sans-serif')
    ax.text(50, 93.8, "End-to-End Data Engineering, Machine Learning Pipeline, FastAPI Backend & Interactive Web Interface",
            ha='center', va='center', fontsize=11, color='#94A3B8', fontfamily='sans-serif')
    
    # Sub-header badges
    ax.text(12, 94.0, "[Author: Qudrat Ullah | TRN-2026-000363]", ha='left', va='center', fontsize=9, color='#38BDF8', fontweight='semibold')
    ax.text(88, 94.0, "[Artifacts: models/pipeline.joblib | data/cleaned/]", ha='right', va='center', fontsize=9, color='#34D399', fontweight='semibold')

    # Helper function for drawing modern cards
    def draw_card(x, y, w, h, title, subtitle, bg_color, border_color, title_color="#F8FAFC"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.2",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=2.0,
            zorder=2
        )
        ax.add_patch(rect)
        # Header strip inside card
        header_rect = patches.FancyBboxPatch(
            (x + 0.3, y + h - 3.2), w - 0.6, 3.0,
            boxstyle="round,pad=0.2,rounding_size=0.8",
            facecolor=border_color,
            edgecolor="none",
            alpha=0.25,
            zorder=3
        )
        ax.add_patch(header_rect)
        ax.text(x + w / 2, y + h - 1.8, title, ha='center', va='center',
                fontsize=11.5, fontweight='bold', color=title_color, zorder=4)
        if subtitle:
            ax.text(x + w / 2, y + h - 4.2, subtitle, ha='center', va='center',
                    fontsize=8.5, color='#94A3B8', fontstyle='italic', zorder=4)

    # Helper function for drawing directional arrows with labels
    def draw_arrow(x1, y1, x2, y2, label="", color="#38BDF8", connectionstyle="arc3,rad=0", label_pos=0.5, label_offset=(0, 1.2)):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=2.2,
                mutation_scale=16,
                connectionstyle=connectionstyle
            ),
            zorder=6
        )
        if label:
            mx = x1 + (x2 - x1) * label_pos + label_offset[0]
            my = y1 + (y2 - y1) * label_pos + label_offset[1]
            ax.text(mx, my, label, ha='center', va='center',
                    fontsize=8, fontweight='bold', color=color,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#0B1120", edgecolor=color, lw=1.0, alpha=0.9),
                    zorder=7)

    # =========================================================================
    # LAYER 1: DATA INGESTION & CLEANING (LEFT COLUMN: x = 3 to 31)
    # =========================================================================
    # Box 1.1: Raw Data Storage
    draw_card(3, 70, 27, 20, "1. RAW DATA STORAGE", "Immutable Historical Records (1970-2024)", "#1E293B", "#38BDF8")
    raw_text = (
        "- File: data/raw/elections.csv\n"
        "- Scope: 24,585 candidate records | 11 elections\n"
        "- Encoding: UTF-8 with BOM (\\ufeff) -> utf-8-sig\n"
        "- Raw Defects:\n"
        "   * 88.6% Nulls in Registered Voters & Turnout\n"
        "   * Text whitespace & party spelling variants\n"
        "   * Negative numbers & invalid percentage values\n"
        "   * Exact duplicate rows across candidate lists"
    )
    ax.text(4.2, 79.5, raw_text, ha='left', va='top', fontsize=8.5, color='#E2E8F0', family='monospace', zorder=5)

    # Box 1.2: Cleaning & Engineering Pipeline (src/cleaning.py)
    draw_card(3, 40, 27, 26, "2. CLEANING & RECOVERY PIPELINE", "6 Deterministic Engineering Stages", "#1E293B", "#60A5FA")
    clean_text = (
        "Module: src/cleaning.py (clean_data)\n\n"
        "[Stage 1] strip_text_columns()\n"
        "  - Strips leading/trailing spaces, title-cases\n"
        "[Stage 2] fix_numeric_types()\n"
        "  - Coerces floats/ints, handles blanks/nulls\n"
        "[Stage 3] standardise_parties()\n"
        "  - Normalizes aliases (PTI, PML-N, PPP, IND)\n"
        "[Stage 4] remove_exact_duplicates()\n"
        "  - Deduplicates identical candidate rows\n"
        "[Stage 5] handle_invalid_and_outliers()\n"
        "  - Drops negative voters and turnout > 100%\n"
        "[Stage 6] handle_missing_values()\n"
        "  - Solves 88.6% missingness by grouping on\n"
        "    ['Year', 'Constituency'] & transform('first')"
    )
    ax.text(4.2, 59.5, clean_text, ha='left', va='top', fontsize=8.2, color='#E2E8F0', family='monospace', zorder=5)

    # Box 1.3: Quality Gate (src/validation.py)
    draw_card(3, 11, 27, 25, "3. AUTOMATED QUALITY GATE", "Strict Integrity Checks Before Model Training", "#1E293B", "#10B981")
    val_text = (
        "Module: src/validation.py (validate_cleaned_data)\n\n"
        "Strict Pre-Condition Assertions:\n"
        " [Check 1] Row Count: len(df) >= 20,000\n"
        " [Check 2] Duplicates: df.duplicated().sum() == 0\n"
        " [Check 3] Valid Voters: Registered Voters > 0\n"
        " [Check 4] Valid Seat Density: 1 <= num_candidates <= 100\n"
        " [Check 5] Categorical Non-Empty: Province, Region, etc.\n"
        " [Check 6] Target Integrity: is_winner in {0, 1}\n\n"
        "Output: data/cleaned/elections_cleaned.csv\n"
        "Status: 24,324 Valid Rows (100% Quality Pass)"
    )
    ax.text(4.2, 29.5, val_text, ha='left', va='top', fontsize=8.2, color='#E2E8F0', family='monospace', zorder=5)

    # Arrows in Column 1
    draw_arrow(16.5, 70, 16.5, 66, "load_raw_data()", "#38BDF8")
    draw_arrow(16.5, 40, 16.5, 36, "quality_gate_check()", "#10B981")

    # =========================================================================
    # LAYER 2: MACHINE LEARNING & MODELING (CENTER COLUMN: x = 36 to 64)
    # =========================================================================
    # Box 2.1: Feature Engineering & Leakage Firewall
    draw_card(36, 70, 28, 20, "4. LEAKAGE FIREWALL & SPLIT", "Temporal Partitioning & Anti-Leakage Audit", "#1E293B", "#F59E0B")
    leak_text = (
        "Module: src/train.py\n\n"
        "[Target Leakage Firewall - Strictly Dropped]:\n"
        "  x Votes (Actual votes cast on polling day)\n"
        "  x vote_share_pct (Post-poll vote percentage)\n"
        "  x log_votes (Log-transformed final tally)\n"
        "  x Turnout N (Recorded election turnout)\n"
        "  x Rejected Votes (Invalid ballot count)\n"
        "  x Candidate Name (Memorization avoidance)\n\n"
        "[Chronological Split]:\n"
        "  - Train Set: 1970 - 2013 (15,879 rows)\n"
        "  - Test Set:  2018 - 2024 (8,445 rows)"
    )
    ax.text(37.2, 79.5, leak_text, ha='left', va='top', fontsize=8.2, color='#E2E8F0', family='monospace', zorder=5)

    # Box 2.2: scikit-learn Pipeline & Training
    draw_card(36, 40, 28, 26, "5. ML PIPELINE & TRAINING", "ColumnTransformer + GradientBoosting", "#1E293B", "#8B5CF6")
    pipe_text = (
        "Module: src/train.py -> models/pipeline.joblib\n\n"
        "[Exact 7 Input Features]:\n"
        "  Numeric (2):  Registered Voters, num_candidates\n"
        "  Categorical (5): Province, Regions 5, Zones 20,\n"
        "                  Party, Six Parties\n\n"
        "[ColumnTransformer Preprocessing]:\n"
        "  * Numeric     -> StandardScaler()\n"
        "  * Categorical -> OneHotEncoder(handle_unknown='ignore')\n\n"
        "[Estimator]: GradientBoostingClassifier\n"
        "  - n_estimators=100, learning_rate=0.1, max_depth=3\n"
        "  - random_state=42 (Deterministic Reproducibility)\n\n"
        "[Artifact]: joblib.dump(pipeline, 'models/pipeline.joblib')"
    )
    ax.text(37.2, 59.5, pipe_text, ha='left', va='top', fontsize=8.2, color='#E2E8F0', family='monospace', zorder=5)

    # Box 2.3: Model Evaluation & Performance Metrics
    draw_card(36, 11, 28, 25, "6. MODEL EVALUATION & METRICS", "Out-of-Time Test Set Performance (2018-2024)", "#1E293B", "#EC4899")
    eval_text = (
        "Out-of-Time Evaluation (Unseen 2018-2024 Tests):\n\n"
        "  * ROC-AUC Score:      0.8903 (High Discriminative Power)\n"
        "  * PR-AUC Score:       0.5958 (Baseline is ~0.11, +440% lift)\n"
        "  * Accuracy:           0.8970 (90% overall seat accuracy)\n"
        "  * Macro F1-Score:     0.7020 (Balanced across classes)\n\n"
        "[Key Confusion Matrix Findings]:\n"
        "  - True Negatives:  7,169 non-winners correctly flagged\n"
        "  - True Posatives:    411 winners correctly predicted\n"
        "  - Class Ratio:     1 winner for every 8 candidates (11%)\n\n"
        "[Concept Drift Note]:\n"
        "  2024 PTI independent candidates ran without symbol."
    )
    ax.text(37.2, 29.5, eval_text, ha='left', va='top', fontsize=8.2, color='#E2E8F0', family='monospace', zorder=5)

    # Arrows in Column 2 & Cross-column connections
    draw_arrow(30, 23.5, 36, 78, "Cleaned CSV", "#F59E0B", connectionstyle="arc3,rad=-0.15")
    draw_arrow(50, 70, 50, 66, "Fit & Transform", "#8B5CF6")
    draw_arrow(50, 40, 50, 36, "Evaluate on Test", "#EC4899")

    # =========================================================================
    # LAYER 3: SERVING, API & FRONTEND (RIGHT COLUMN: x = 69 to 97)
    # =========================================================================
    # Box 3.1: FastAPI Production Backend (src/api.py)
    draw_card(69, 56, 28, 34, "7. FASTAPI BACKEND SERVER", "High-Performance ASGI REST API (src/api.py)", "#1E293B", "#06B6D4")
    api_text = (
        "Framework: FastAPI + Uvicorn ASGI Server\n"
        "Lifespan Startup: Loads models/pipeline.joblib once\n\n"
        "[REST Endpoints]:\n"
        "  1. GET /         -> Serves HTML5 frontend application\n"
        "  2. GET /health   -> {'status': 'ok', 'model_loaded': true}\n"
        "  3. GET /metadata -> Returns sorted unique lists and\n"
        "                      cascading hierarchy for dropdowns:\n"
        "                      Province -> Regions 5 -> Zones 20\n"
        "  4. POST /predict -> Validates via Pydantic CandidateInput\n"
        "                      Returns win_probability & outcome label\n"
        "  5. POST /predict-batch -> Accepts CSV upload, validates,\n"
        "                      scores rows, streams scored CSV file"
    )
    ax.text(70.2, 81.5, api_text, ha='left', va='top', fontsize=8.2, color='#E2E8F0', family='monospace', zorder=5)

    # Box 3.2: Interactive Frontend UI (frontend/index.html)
    draw_card(69, 11, 28, 41, "8. INTERACTIVE FRONTEND UI", "Modern Responsive Single Page Application (SPA)", "#1E293B", "#F43F5E")
    ui_text = (
        "Architecture: Clean HTML5, CSS3 Glassmorphism, Vanilla JS\n\n"
        "[Candidate Simulator Panel]:\n"
        "  - Dynamic Cascading Dropdowns:\n"
        "    Province -> Macro Region (5) -> Electoral Zone (20)\n"
        "  - Party Blocs: Auto-syncs Six Parties with Party selection\n"
        "  - Numeric inputs: Registered Voters (up to 10M), Candidates\n"
        "  - Instant Preset Buttons (Lahore PMLN, Peshawar PTI, etc.)\n\n"
        "[Visual Prediction Gauge]:\n"
        "  - Win Probability (%) with animated progress bar\n"
        "  - Dynamic badge: 'Likely Winner' vs 'Likely Loss'\n\n"
        "[Batch CSV Testing Panel]:\n"
        "  - Drag-and-drop CSV file upload\n"
        "  - Real-time scoring via /predict-batch\n"
        "  - One-click scored CSV file download"
    )
    ax.text(70.2, 43.5, ui_text, ha='left', va='top', fontsize=8.2, color='#E2E8F0', family='monospace', zorder=5)

    # Arrow from Model to FastAPI
    draw_arrow(64, 53, 69, 73, "Load Pipeline Artifact", "#06B6D4", connectionstyle="arc3,rad=-0.1")
    # Arrow between API and UI
    draw_arrow(83, 56, 83, 52, "HTTP JSON & CSV", "#F43F5E")

    # =========================================================================
    # FOOTER: DEPLOYMENT & CONTAINERIZATION (BOTTOM STRIP: x = 3 to 97, y = 1 to 8)
    # =========================================================================
    footer_rect = patches.FancyBboxPatch(
        (3, 1.2), 94, 7.5,
        boxstyle="round,pad=0.5,rounding_size=1.0",
        facecolor="#111827",
        edgecolor="#475569",
        linewidth=1.5,
        zorder=2
    )
    ax.add_patch(footer_rect)
    
    ax.text(5, 6.2, "9. CONTAINERIZATION & FREE CLOUD DEPLOYMENT ARCHITECTURE", fontsize=10.5, fontweight='bold', color='#38BDF8', zorder=4)
    deploy_summary = (
        "- Dockerfile: python:3.12-slim base image | Installs requirements.txt | Exposes Port 7860 | Launches via uvicorn src.api:app --host 0.0.0.0 --port 7860\n"
        "- Cloud Options: Free Hugging Face Spaces (Docker SDK) or Render Free Web Service. Both provide 24/7 public HTTPS URLs without requiring local PC to stay on.\n"
        "- Git Tracking: .gitignore explicitly whitelists !models/pipeline.joblib and !models/ so pre-trained weights deploy seamlessly with the code."
    )
    ax.text(5, 4.8, deploy_summary, fontsize=8.2, color='#CBD5E1', family='monospace', va='top', zorder=4)

    plt.tight_layout()
    fig.savefig(OUTPUT_IMG, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none', dpi=150)
    plt.close(fig)
    print(f"Architecture diagram generated successfully at: {OUTPUT_IMG}")

if __name__ == "__main__":
    create_architecture_diagram()
