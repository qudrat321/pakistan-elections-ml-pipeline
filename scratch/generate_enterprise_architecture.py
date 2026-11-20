# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Generates an Enterprise Solution Architect-Grade Medallion Architecture diagram at 300 DPI."""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"
OUTPUT_IMG = FIGURES_DIR / "05_system_architecture.png"

def create_enterprise_architecture():
    # 13.5 x 8.5 inches at 300 DPI = 4050 x 2550 px (Ultra-sharp, crystal clear)
    fig, ax = plt.subplots(figsize=(13.5, 8.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')  # Clean light executive canvas
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Top Executive Header Banner
    ax.text(50, 97.2, "ENTERPRISE SOLUTION ARCHITECTURE: PAKISTAN ELECTIONS ML PIPELINE",
            ha='center', va='center', fontsize=14.5, fontweight='bold', color='#0F172A', fontfamily='sans-serif')
    ax.text(50, 94.6, "End-to-End Medallion Lakehouse Pattern with Decoupled REST Inference Microservice & Interactive Web UI",
            ha='center', va='center', fontsize=9.2, color='#475569', fontfamily='sans-serif')
    
    # Metadata badges
    ax.text(5, 95.0, "SYSTEM: PRODUCTION-GRADE ML PIPELINE", fontsize=7.5, fontweight='bold', color='#0284C7')
    ax.text(95, 95.0, "AUTHOR: QUDRAT ULLAH (TRN-2026-000363)", ha='right', fontsize=7.5, fontweight='bold', color='#059669')

    # Line divider
    ax.plot([4, 96], [93.2, 93.2], color='#CBD5E1', lw=1.2, zorder=2)

    # =========================================================================
    # SWIMLANE 1: BRONZE TIER (RAW INGESTION ZONE) - x: 4 to 24
    # =========================================================================
    # Lane Box
    lane1 = patches.FancyBboxPatch((4, 16), 21, 74, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  facecolor="#FFFFFF", edgecolor="#B45309", linewidth=2.0, zorder=2)
    ax.add_patch(lane1)
    # Lane Header Strip
    h1 = patches.FancyBboxPatch((4.2, 85.5), 20.6, 4.2, boxstyle="round,pad=0.2,rounding_size=0.6",
                                facecolor="#B45309", edgecolor="none", zorder=3)
    ax.add_patch(h1)
    ax.text(14.5, 88.2, "1. BRONZE TIER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(14.5, 86.4, "Raw Landing Zone (Immutable)", ha='center', va='center', fontsize=7.2, color='#FEF3C7', zorder=4)

    # Box 1.1: Raw Storage Artifact
    b1_1 = patches.FancyBboxPatch((5.5, 53), 18, 30, boxstyle="round,pad=0.4,rounding_size=0.8",
                                  facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.4, zorder=3)
    ax.add_patch(b1_1)
    ax.text(14.5, 80.5, "Raw Gazette Dataset", ha='center', va='center', fontsize=9.0, fontweight='bold', color='#92400E', zorder=4)
    ax.text(14.5, 78.2, "data/raw/elections.csv", ha='center', va='center', fontsize=7.2, family='monospace', color='#B45309', zorder=4)
    b1_1_text = (
        "• Scope: 24,585 Records\n"
        "• Span: 11 Elections (1970–2024)\n"
        "• Source: Official ECP Gazettes\n"
        "• Format: CSV (UTF-8 with BOM)\n"
        "• Access: Strict Read-Only\n"
        "• Raw Imperfections Identified:\n"
        "   - Byte Order Mark (\ufeff)\n"
        "   - 88.6% Nulls in Seat Metrics\n"
        "   - Duplicate Candidate Rows\n"
        "   - Unstandardized Parties"
    )
    ax.text(6.8, 75.5, b1_1_text, ha='left', va='top', fontsize=7.2, color='#78350F', family='sans-serif', zorder=4)

    # Box 1.2: Ingestion Adapter
    b1_2 = patches.FancyBboxPatch((5.5, 18), 18, 31, boxstyle="round,pad=0.4,rounding_size=0.8",
                                  facecolor="#FFFFFF", edgecolor="#B45309", linewidth=1.2, zorder=3)
    ax.add_patch(b1_2)
    ax.text(14.5, 46.5, "Safe Ingestion Adapter", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#0F172A', zorder=4)
    ax.text(14.5, 44.5, "src/load_data.py", ha='center', va='center', fontsize=7.2, family='monospace', color='#0284C7', zorder=4)
    b1_2_text = (
        "• Function: load_raw_data()\n"
        "• Protocol: pandas.read_csv()\n"
        "• Encoding: 'utf-8-sig'\n"
        "  (Strips \\ufeff BOM byte prefix)\n"
        "• Error Handling:\n"
        "  Raises explicit FileNotFoundError\n"
        "  if gazette is missing.\n"
        "• Output Contract:\n"
        "  Immutable In-Memory DataFrame\n"
        "  passed directly to Silver tier."
    )
    ax.text(6.8, 42.0, b1_2_text, ha='left', va='top', fontsize=7.0, color='#334155', family='sans-serif', zorder=4)

    # Arrow 1.1 -> 1.2
    ax.annotate("", xy=(14.5, 50), xytext=(14.5, 53),
                arrowprops=dict(arrowstyle="-|>", color="#B45309", lw=1.5), zorder=5)

    # =========================================================================
    # SWIMLANE 2: SILVER TIER (CLEANING & QUALITY GATE) - x: 28 to 48
    # =========================================================================
    lane2 = patches.FancyBboxPatch((28, 16), 21, 74, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  facecolor="#FFFFFF", edgecolor="#0284C7", linewidth=2.0, zorder=2)
    ax.add_patch(lane2)
    h2 = patches.FancyBboxPatch((28.2, 85.5), 20.6, 4.2, boxstyle="round,pad=0.2,rounding_size=0.6",
                                facecolor="#0284C7", edgecolor="none", zorder=3)
    ax.add_patch(h2)
    ax.text(38.5, 88.2, "2. SILVER TIER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(38.5, 86.4, "Curated & Validated Zone", ha='center', va='center', fontsize=7.2, color='#E0F2FE', zorder=4)

    # Box 2.1: Cleaning Pipeline Engine
    b2_1 = patches.FancyBboxPatch((29.5, 48), 18, 35, boxstyle="round,pad=0.4,rounding_size=0.8",
                                  facecolor="#F0F9FF", edgecolor="#0284C7", linewidth=1.4, zorder=3)
    ax.add_patch(b2_1)
    ax.text(38.5, 80.5, "6-Stage Cleaning Engine", ha='center', va='center', fontsize=9.0, fontweight='bold', color='#0369A1', zorder=4)
    ax.text(38.5, 78.2, "src/cleaning.py", ha='center', va='center', fontsize=7.2, family='monospace', color='#0284C7', zorder=4)
    b2_1_text = (
        "[S1] strip_text_columns()\n"
        "  - Cleans strings & spaces\n"
        "[S2] fix_numeric_types()\n"
        "  - Casts floats/ints strictly\n"
        "[S3] standardise_parties()\n"
        "  - Maps PMLN, PTI, PPP aliases\n"
        "[S4] remove_exact_duplicates()\n"
        "  - Eliminates duplicate entries\n"
        "[S5] handle_invalid_outliers()\n"
        "  - Filters impossible numbers\n"
        "[S6] handle_missing_values()\n"
        "  - Solves 88.6% nulls by\n"
        "    grouping ['Year','Seat'] &\n"
        "    transform('first') backfill!"
    )
    ax.text(30.8, 75.5, b2_1_text, ha='left', va='top', fontsize=6.8, color='#0C4A6E', family='monospace', zorder=4)

    # Box 2.2: Automated Quality Gate
    b2_2 = patches.FancyBboxPatch((29.5, 18), 18, 27, boxstyle="round,pad=0.4,rounding_size=0.8",
                                  facecolor="#ECFDF5", edgecolor="#059669", linewidth=1.4, zorder=3)
    ax.add_patch(b2_2)
    ax.text(38.5, 42.5, "Automated Quality Gate", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#065F46', zorder=4)
    ax.text(38.5, 40.5, "src/validation.py", ha='center', va='center', fontsize=7.2, family='monospace', color='#059669', zorder=4)
    b2_2_text = (
        "• 6 Strict Assertions Barrier:\n"
        "  ✓ Row Count >= 20,000\n"
        "  ✓ Duplicates == 0\n"
        "  ✓ Registered Voters > 0\n"
        "  ✓ Seat Density: 1 to 100\n"
        "  ✓ Categoricals Non-Empty\n"
        "  ✓ Target is_winner in {0,1}\n"
        "• Clean Output Saved to Disk:\n"
        "  data/cleaned/elections_cleaned.csv\n"
        "  (24,324 Clean Rows, 100% Pass)"
    )
    ax.text(30.8, 38.5, b2_2_text, ha='left', va='top', fontsize=6.8, color='#064E3B', family='sans-serif', zorder=4)

    # Arrow 2.1 -> 2.2
    ax.annotate("", xy=(38.5, 46), xytext=(38.5, 48),
                arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=1.5), zorder=5)

    # Connect Bronze -> Silver
    ax.annotate("", xy=(28, 64), xytext=(25, 64),
                arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=2.0), zorder=5)
    ax.text(26.5, 66.0, "Raw CSV", ha='center', va='center', fontsize=6.8, fontweight='bold', color="#0284C7",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="#0284C7", lw=0.7), zorder=6)

    # =========================================================================
    # SWIMLANE 3: GOLD TIER (MACHINE LEARNING & REGISTRY) - x: 52 to 72
    # =========================================================================
    lane3 = patches.FancyBboxPatch((52, 16), 21, 74, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  facecolor="#FFFFFF", edgecolor="#7C3AED", linewidth=2.0, zorder=2)
    ax.add_patch(lane3)
    h3 = patches.FancyBboxPatch((52.2, 85.5), 20.6, 4.2, boxstyle="round,pad=0.2,rounding_size=0.6",
                                facecolor="#7C3AED", edgecolor="none", zorder=3)
    ax.add_patch(h3)
    ax.text(62.5, 88.2, "3. GOLD TIER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(62.5, 86.4, "ML Pipeline & Model Registry", ha='center', va='center', fontsize=7.2, color='#EDE9FE', zorder=4)

    # Box 3.1: Leakage Firewall & Temporal Split
    b3_1 = patches.FancyBboxPatch((53.5, 52), 18, 31, boxstyle="round,pad=0.4,rounding_size=0.8",
                                  facecolor="#FAF5FF", edgecolor="#7C3AED", linewidth=1.4, zorder=3)
    ax.add_patch(b3_1)
    ax.text(62.5, 80.5, "Anti-Leakage Firewall", ha='center', va='center', fontsize=9.0, fontweight='bold', color='#5B21B6', zorder=4)
    ax.text(62.5, 78.2, "src/train.py", ha='center', va='center', fontsize=7.2, family='monospace', color='#7C3AED', zorder=4)
    b3_1_text = (
        "• Strict Leakage Column Purge:\n"
        "  - Votes (Actual votes cast)\n"
        "  - vote_share_pct (Vote share)\n"
        "  - Turnout N (Recorded turnout)\n"
        "  - Rejected Votes (Disqualified)\n"
        "  - Candidate Name (Memorization)\n"
        "• Chronological Split Method:\n"
        "  - Train: 1970–2013 (15,879 rows)\n"
        "  - Test:  2018–2024 (8,445 rows)\n"
        "• Prevents Temporal Leakage!"
    )
    ax.text(54.8, 75.5, b3_1_text, ha='left', va='top', fontsize=6.8, color='#4C1D95', family='sans-serif', zorder=4)

    # Box 3.2: scikit-learn Pipeline Registry
    b3_2 = patches.FancyBboxPatch((53.5, 18), 18, 31, boxstyle="round,pad=0.4,rounding_size=0.8",
                                  facecolor="#FFFFFF", edgecolor="#7C3AED", linewidth=1.2, zorder=3)
    ax.add_patch(b3_2)
    ax.text(62.5, 46.5, "Serialized Model Registry", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#0F172A', zorder=4)
    ax.text(62.5, 44.5, "models/pipeline.joblib", ha='center', va='center', fontsize=7.2, family='monospace', color='#059669', zorder=4)
    b3_2_text = (
        "• Unified Atomic Pipeline:\n"
        "  ColumnTransformer(\n"
        "    Numeric: StandardScaler(),\n"
        "    Categoric: OneHotEncoder(\n"
        "      handle_unknown='ignore'))\n"
        "• Estimator: GradientBoosting(\n"
        "    n_estimators=100, depth=3,\n"
        "    learning_rate=0.1, seed=42)\n"
        "• Performance on Test Set:\n"
        "  - PR-AUC: 0.5958 (+440%)\n"
        "  - ROC-AUC: 0.8903 (High)"
    )
    ax.text(54.8, 42.0, b3_2_text, ha='left', va='top', fontsize=6.7, color='#334155', family='sans-serif', zorder=4)

    # Arrow 3.1 -> 3.2
    ax.annotate("", xy=(62.5, 50), xytext=(62.5, 52),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=1.5), zorder=5)

    # Connect Silver -> Gold
    ax.annotate("", xy=(52, 64), xytext=(49, 64),
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2.0), zorder=5)
    ax.text(50.5, 66.0, "Clean Data", ha='center', va='center', fontsize=6.8, fontweight='bold', color="#059669",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="#059669", lw=0.7), zorder=6)

    # =========================================================================
    # SWIMLANE 4: PLATINUM / SERVING TIER (API & FRONTEND) - x: 76 to 96
    # =========================================================================
    lane4 = patches.FancyBboxPatch((76, 16), 20, 74, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  facecolor="#FFFFFF", edgecolor="#059669", linewidth=2.0, zorder=2)
    ax.add_patch(lane4)
    h4 = patches.FancyBboxPatch((76.2, 85.5), 19.6, 4.2, boxstyle="round,pad=0.2,rounding_size=0.6",
                                facecolor="#059669", edgecolor="none", zorder=3)
    ax.add_patch(h4)
    ax.text(86.0, 88.2, "4. PLATINUM TIER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(86.0, 86.4, "Serving, API & UI Simulator", ha='center', va='center', fontsize=7.2, color='#D1FAE5', zorder=4)

    # Box 4.1: FastAPI Production Backend
    b4_1 = patches.FancyBboxPatch((77.2, 51), 17.6, 32, boxstyle="round,pad=0.4,rounding_size=0.8",
                                  facecolor="#F0FDF4", edgecolor="#059669", linewidth=1.4, zorder=3)
    ax.add_patch(b4_1)
    ax.text(86.0, 80.5, "FastAPI Microservice", ha='center', va='center', fontsize=9.0, fontweight='bold', color='#065F46', zorder=4)
    ax.text(86.0, 78.2, "src/api.py (ASGI Uvicorn)", ha='center', va='center', fontsize=7.2, family='monospace', color='#0284C7', zorder=4)
    b4_1_text = (
        "• Lifespan Startup Management:\n"
        "  Loads pipeline.joblib once\n"
        "  into RAM for sub-10ms latency\n"
        "• REST Endpoints Implemented:\n"
        "  - GET / : Serves HTML5 SPA\n"
        "  - GET /health : Status probe\n"
        "  - GET /metadata : Hierarchy map\n"
        "  - POST /predict : Pydantic JSON\n"
        "  - POST /predict-batch : Upload\n"
        "    CSV & stream scored file"
    )
    ax.text(78.2, 75.5, b4_1_text, ha='left', va='top', fontsize=6.8, color='#064E3B', family='sans-serif', zorder=4)

    # Box 4.2: Interactive Web UI Frontend
    b4_2 = patches.FancyBboxPatch((77.2, 18), 17.6, 30, boxstyle="round,pad=0.4,rounding_size=0.8",
                                  facecolor="#FFFFFF", edgecolor="#059669", linewidth=1.2, zorder=3)
    ax.add_patch(b4_2)
    ax.text(86.0, 45.5, "Single Page App (UI)", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#0F172A', zorder=4)
    ax.text(86.0, 43.5, "frontend/index.html", ha='center', va='center', fontsize=7.2, family='monospace', color='#E11D48', zorder=4)
    b4_2_text = (
        "• Cascading Dropdown Engine:\n"
        "  Province -> Region -> Zone\n"
        "• Candidate Feature Simulator:\n"
        "  Voters up to 1 Crore (10M)\n"
        "• Live Win Probability Gauge:\n"
        "  Animated bar + status badge\n"
        "• Batch CSV Testing Panel:\n"
        "  Drag-and-drop file scoring"
    )
    ax.text(78.2, 40.5, b4_2_text, ha='left', va='top', fontsize=6.8, color='#334155', family='sans-serif', zorder=4)

    # Arrow 4.1 -> 4.2
    ax.annotate("", xy=(86.0, 49), xytext=(86.0, 51),
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=1.5), zorder=5)

    # Connect Gold -> Platinum
    ax.annotate("", xy=(76, 64), xytext=(73, 64),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=2.0), zorder=5)
    ax.text(74.5, 66.0, "Model File", ha='center', va='center', fontsize=6.8, fontweight='bold', color="#7C3AED",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="#7C3AED", lw=0.7), zorder=6)

    # =========================================================================
    # BOTTOM CROSS-CUTTING TIER: DEPLOYMENT & DEVOPS - y: 3 to 13
    # =========================================================================
    dev_box = patches.FancyBboxPatch((4, 3.5), 92, 10.5, boxstyle="round,pad=0.4,rounding_size=0.8",
                                     facecolor="#0F172A", edgecolor="#38BDF8", linewidth=1.5, zorder=2)
    ax.add_patch(dev_box)
    ax.text(5.5, 11.5, "5. CROSS-CUTTING CONCERNS: CONTAINERIZATION, CLOUD DEPLOYMENT & TEST HARNESS",
            fontsize=8.5, fontweight='bold', color='#38BDF8', zorder=3)

    infra_text = (
        "• Docker Containerization: python:3.12-slim base image | Pinned requirements.txt | Exposes Port 7860 | Launches via uvicorn src.api:app --host 0.0.0.0 --port 7860\n"
        "• Zero-Cost Cloud Hosting: Hugging Face Spaces (Docker SDK) or Render Web Services provide 24/7 public HTTPS endpoints with zero local hardware requirements.\n"
        "• Quality Assurance & CI/CD: 14 automated unit & integration tests executed via pytest verifying cleaning rules, quality gate assertions, and API schemas."
    )
    ax.text(5.5, 9.8, infra_text, fontsize=6.8, color='#CBD5E1', family='monospace', va='top', zorder=3)

    plt.tight_layout()
    fig.savefig(OUTPUT_IMG, bbox_inches='tight', facecolor='#F8FAFC', edgecolor='none', dpi=300)
    plt.close(fig)
    print(f"Enterprise Solution Architecture Diagram generated at: {OUTPUT_IMG}")

if __name__ == "__main__":
    create_enterprise_architecture()
