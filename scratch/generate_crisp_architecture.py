# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Generates an ultra-crisp, high-contrast, razor-sharp 300 DPI architecture diagram for IEEE documentation."""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"
OUTPUT_IMG = FIGURES_DIR / "05_system_architecture.png"

def create_crisp_architecture():
    # 9.6 x 6.6 inches at 300 DPI = 2880 x 1980 px (Ultra High Resolution, Razor Sharp)
    fig, ax = plt.subplots(figsize=(10.2, 7.0), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header Banner (IEEE Style, Clean High-Contrast Slate/Navy)
    ax.text(50, 97.2, "PAKISTAN ELECTIONS ML PIPELINE: 9-COMPONENT ARCHITECTURE",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='#0F172A', fontfamily='sans-serif')
    ax.text(50, 94.2, "End-to-End Topology: Gazette Ingestion -> Cleaning -> Quality Gate -> Leak-Free ML -> FastAPI -> Web UI",
            ha='center', va='center', fontsize=8.5, color='#475569', fontfamily='sans-serif')

    # Card Drawing Helper
    def draw_component_card(x, y, w, h, step_num, title, subtitle, items, border_col, header_bg):
        # Card Background
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.4,rounding_size=0.8",
            facecolor="#F8FAFC",
            edgecolor=border_col,
            linewidth=1.8,
            zorder=2
        )
        ax.add_patch(card)

        # Header Ribbon
        h_strip = patches.FancyBboxPatch(
            (x + 0.1, y + h - 2.8), w - 0.2, 2.7,
            boxstyle="round,pad=0.1,rounding_size=0.6",
            facecolor=header_bg,
            edgecolor="none",
            zorder=3
        )
        ax.add_patch(h_strip)

        # Header Title
        ax.text(x + w / 2, y + h - 1.4, f"[{step_num}] {title}", ha='center', va='center',
                fontsize=8.8, fontweight='bold', color='#FFFFFF', zorder=4)

        # Subtitle
        if subtitle:
            ax.text(x + w / 2, y + h - 3.8, subtitle, ha='center', va='center',
                    fontsize=7.2, fontweight='bold', color=border_col, zorder=4)

        # Content bullets
        text_y = y + h - 5.4
        for item in items:
            ax.text(x + 1.2, text_y, item, ha='left', va='top',
                    fontsize=7.0, color='#1E293B', fontfamily='sans-serif', zorder=4)
            text_y -= 2.2

    # Draw Arrows
    def draw_flow_arrow(x1, y1, x2, y2, label="", color="#0284c7"):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=2.0,
                mutation_scale=13,
            ),
            zorder=5
        )
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2 + 1.2
            ax.text(mx, my, label, ha='center', va='center',
                    fontsize=6.8, fontweight='bold', color=color,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=color, lw=0.8),
                    zorder=6)

    # =========================================================================
    # ROW 1: DATA ENGINEERING (y = 66 to 90)
    # =========================================================================
    # 1. Raw Data
    c1_items = [
        "• Path: data/raw/elections.csv",
        "• Scope: 24,585 rows | 11 Elections (1970-2024)",
        "• Encoding: UTF-8 BOM (\ufeff) handled",
        "• Status: Read-Only Immutable Gazette"
    ]
    draw_component_card(2, 67, 30, 24, "1", "RAW DATA STORAGE", "data/raw/ (Immutable)", c1_items, "#0284C7", "#0369A1")

    # 2. Cleaning Pipeline
    c2_items = [
        "• Module: src/cleaning.py (6 Stages)",
        "• Strip whitespace & fix types (int/float)",
        "• Standardize party names & drop duplicates",
        "• Groupby ['Year','Constituency'] to fill nulls"
    ]
    draw_component_card(35, 67, 30, 24, "2", "CLEANING PIPELINE", "6 Deterministic Stages", c2_items, "#0D9488", "#0F766E")

    # 3. Quality Gate
    c3_items = [
        "• Module: src/validation.py (6 Assertions)",
        "• Row count >= 20,000 | Zero duplicates",
        "• Positive registered voters & valid seats",
        "• Out: data/cleaned/elections_cleaned.csv"
    ]
    draw_component_card(68, 67, 30, 24, "3", "QUALITY GATE", "100% Automated Validation", c3_items, "#16A34A", "#15803D")

    # Row 1 Arrows
    draw_flow_arrow(32, 79, 35, 79, "utf-8-sig", "#0284C7")
    draw_flow_arrow(65, 79, 68, 79, "24,324 rows", "#0D9488")

    # =========================================================================
    # ROW 2: MACHINE LEARNING & EVALUATION (y = 37 to 61)
    # =========================================================================
    # 4. Leakage Firewall & Split
    c4_items = [
        "• Drops: Votes, Turnout, Rejected Votes",
        "• Drops: Candidate Name (Memorization)",
        "• Train Set: 1970–2013 (15,879 rows)",
        "• Test Set:  2018–2024 (8,445 rows)"
    ]
    draw_component_card(2, 38, 30, 24, "4", "LEAKAGE FIREWALL & SPLIT", "Temporal Anti-Leakage Split", c4_items, "#D97706", "#B45309")

    # 5. scikit-learn Pipeline
    c5_items = [
        "• Module: src/train.py",
        "• ColumnTransformer (OHE + Scaler)",
        "• Estimator: GradientBoostingClassifier",
        "• Artifact: models/pipeline.joblib"
    ]
    draw_component_card(35, 38, 30, 24, "5", "ML PIPELINE ARTIFACT", "ColumnTransformer + GBDT", c5_items, "#7C3AED", "#6D28D9")

    # 6. Evaluation & Diagnostics
    c6_items = [
        "• PR-AUC: 0.5958 (+440% over baseline)",
        "• ROC-AUC: 0.8903 (High discrimination)",
        "• Top Feature: Political Party (~0.14 drop)",
        "• Concept Drift: 2024 PTI Independent Symbols"
    ]
    draw_component_card(68, 38, 30, 24, "6", "MODEL EVALUATION", "Held-Out Test Set Metrics", c6_items, "#DB2777", "#BE185D")

    # Down from Quality Gate to Firewall
    ax.annotate("", xy=(17, 62), xytext=(83, 67),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=1.8, connectionstyle="arc3,rad=-0.15"), zorder=5)
    ax.text(50, 64.5, "Verified Clean Data", ha='center', va='center', fontsize=6.8, fontweight='bold', color="#16A34A",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#16A34A", lw=0.8), zorder=6)

    # Row 2 Arrows
    draw_flow_arrow(32, 50, 35, 50, "7 Features", "#D97706")
    draw_flow_arrow(65, 50, 68, 50, "Test 2018-24", "#7C3AED")

    # =========================================================================
    # ROW 3: FASTAPI BACKEND, FRONTEND & CLOUD DEPLOY (y = 8 to 32)
    # =========================================================================
    # 7. FastAPI Backend
    c7_items = [
        "• Module: src/api.py (Uvicorn ASGI)",
        "• Lifespan: Loads model once into RAM",
        "• GET /metadata: Cascading hierarchy",
        "• POST /predict: Pydantic validation",
        "• POST /predict-batch: Scored CSV stream"
    ]
    draw_component_card(2, 9, 30, 24, "7", "FASTAPI BACKEND", "High-Performance REST API", c7_items, "#0891B2", "#0E7490")

    # 8. Interactive Frontend UI
    c8_items = [
        "• Path: frontend/index.html (Vanilla SPA)",
        "• Cascading: Province -> Region -> Zone",
        "• Party Blocs: Auto-syncs alliance",
        "• Real-Time Win Gauge & Probability",
        "• Drag-and-drop batch CSV testing"
    ]
    draw_component_card(35, 9, 30, 24, "8", "INTERACTIVE FRONTEND", "Zero-Dependency HTML5/JS UI", c8_items, "#E11D48", "#BE123C")

    # 9. Docker & Cloud Deployment
    c9_items = [
        "• Dockerfile: python:3.12-slim base",
        "• Exposes: Port 7860 (Hugging Face / Render)",
        "• Zero-Cost 24/7 Cloud Availability",
        "• .gitignore: !models/pipeline.joblib"
    ]
    draw_component_card(68, 9, 30, 24, "9", "CLOUD DEPLOYMENT", "Docker Container (Port 7860)", c9_items, "#4F46E5", "#4338CA")

    # Connecting ML Model to FastAPI
    ax.annotate("", xy=(17, 33), xytext=(50, 38),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=1.8, connectionstyle="arc3,rad=-0.12"), zorder=5)
    ax.text(33.5, 35.5, "Lifespan Model Load", ha='center', va='center', fontsize=6.8, fontweight='bold', color="#7C3AED",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#7C3AED", lw=0.8), zorder=6)

    # Row 3 Arrows
    draw_flow_arrow(32, 21, 35, 21, "JSON / Stream", "#0891B2")
    draw_flow_arrow(65, 21, 68, 21, "Docker Build", "#E11D48")

    # Footer note
    ax.text(50, 4.0, "Verified Architecture | 14/14 Pytest Unit Tests Passing | Author: Qudrat Ullah (TRN-2026-000363)",
            ha='center', va='center', fontsize=7.2, color='#64748B', fontstyle='italic')

    plt.tight_layout()
    fig.savefig(OUTPUT_IMG, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none', dpi=300)
    plt.close(fig)
    print(f"Crisp 300 DPI architecture diagram generated at: {OUTPUT_IMG}")

if __name__ == "__main__":
    create_crisp_architecture()
