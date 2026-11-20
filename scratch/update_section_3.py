# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Replaces Section III in scratch/build_master_handbook.py with enterprise solution architect content."""

new_sec3 = '''    # =========================================================================
    # SECTION III: SYSTEM ARCHITECTURE & MEDALLION DATA FLOW
    # =========================================================================
    story.append(Paragraph("III. System Architecture & Medallion Data Flow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    story.append(Paragraph("A. Enterprise Solution Architecture Topology", h2_style))
    story.append(
        Paragraph(
            "Fig. 1 depicts the complete enterprise solution architecture of the Pakistan Elections ML Pipeline. "
            "Designed according to modern lakehouse and decoupled microservice patterns, the system partitions "
            "data lifecycle responsibilities across four distinct Medallion architectural tiers (Bronze, Silver, Gold, Platinum) "
            "and an overarching Cross-Cutting Infrastructure tier. Every component operates with strict boundary isolation, "
            "explicit data contracts, and deterministic reproducibility controls.",
            body,
        )
    )

    if (FIGURES_DIR / "05_system_architecture.png").exists():
        story.append(KeepTogether([
            Image(str(FIGURES_DIR / "05_system_architecture.png"), width=6.9 * inch, height=4.35 * inch),
            Spacer(1, 2),
            Paragraph(
                "<b>Fig. 1.</b> Enterprise Solution Architecture & Medallion Data Flow Topology. "
                "Illustrates the end-to-end data lifecycle across Bronze, Silver, Gold, Platinum, and Cross-Cutting Infrastructure tiers.",
                caption_style,
            )
        ]))

    story.append(Paragraph("B. Medallion Architecture Tiers & Formal Data Contracts", h2_style))
    story.append(
        Paragraph(
            "The table below establishes the formal data contracts, storage targets, transformation mechanisms, "
            "and quality SLAs enforced across each tier of the Medallion architecture:",
            body,
        )
    )

    medallion_table = [
        [Paragraph("Medallion Tier", tbl_header), Paragraph("Architectural Role", tbl_header), Paragraph("Storage Artifact", tbl_header), Paragraph("Data Contract & Transformation", tbl_header), Paragraph("Quality Gate & SLA", tbl_header)],
        [Paragraph("1. Bronze Tier", tbl_mono), Paragraph("Raw Landing Zone", tbl_text), Paragraph("data/raw/elections.csv", tbl_mono), Paragraph("Official digitized ECP gazettes across 11 elections (1970–2024). Ingested via utf-8-sig to strip BOM prefix.", tbl_text), Paragraph("Read-only immutable file; 24,585 historical records preserved.", tbl_text)],
        [Paragraph("2. Silver Tier", tbl_mono), Paragraph("Curated & Cleaned Zone", tbl_text), Paragraph("data/cleaned/ elections_cleaned.csv", tbl_mono), Paragraph("6-stage deterministic cleaning engine (src/cleaning.py). Resolves 88.6% nulls by grouping ['Year','Seat'] & backfilling.", tbl_text), Paragraph("100% Quality Gate pass (src/validation.py): 6 assertions, 24,324 verified rows.", tbl_text)],
        [Paragraph("3. Gold Tier", tbl_mono), Paragraph("Feature Store & Registry", tbl_text), Paragraph("models/pipeline.joblib", tbl_mono), Paragraph("Temporal anti-leakage split (1970–2013 train / 2018–2024 test). ColumnTransformer (OHE + Scaler) + GradientBoosting.", tbl_text), Paragraph("PR-AUC: 0.5958 (+440% lift); ROC-AUC: 0.8903. Pinned random_state=42.", tbl_text)],
        [Paragraph("4. Platinum Tier", tbl_mono), Paragraph("Serving & Presentation", tbl_text), Paragraph("src/api.py & frontend/index.html", tbl_mono), Paragraph("FastAPI ASGI REST microservice + Vanilla JS SPA. Lifespan in-memory model cache; Pydantic JSON validation.", tbl_text), Paragraph("Sub-10ms single prediction latency; streaming batch CSV scoring engine.", tbl_text)],
        [Paragraph("5. Cross-Cutting", tbl_mono), Paragraph("DevOps & Infrastructure", tbl_text), Paragraph("Dockerfile & tests/", tbl_mono), Paragraph("Multi-stage Docker container (python:3.12-slim) exposing Port 7860. Automated pytest CI harness (14 tests).", tbl_text), Paragraph("Zero-cost 24/7 cloud hosting on Hugging Face Spaces or Render Web Service.", tbl_text)],
    ]
    t_med = Table(medallion_table, colWidths=[65, 80, 105, 144, 110])
    t_med.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), c_primary),
                ("BOX", (0, 0), (-1, -1), 1, c_border),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ]
        )
    )
    story.append(t_med)
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Inter-Component Communication & Protocol Topology", h2_style))
    story.append(
        Paragraph(
            "A professional architecture must document how components communicate across process boundaries: "
            "<br/>• <b>Storage-to-Memory Ingestion:</b> <font name='Courier'>src/load_data.py</font> reads the raw gazette from local storage "
            "using pandas with <font name='Courier'>encoding='utf-8-sig'</font>, safely decoding the Unicode BOM prefix without corrupting headers. "
            "<br/>• <b>Data Transformation Pipeline:</b> The 6 cleaning stages in <font name='Courier'>src/cleaning.py</font> execute as pure "
            "in-memory vectorized transformations, passing immutable DataFrame instances between stages to eliminate side-effects. "
            "<br/>• <b>Quality Gate Verification Barrier:</b> Before writing to disk, <font name='Courier'>src/validation.py</font> executes "
            "as a blocking gate. If any integrity assertion fails, an unhandled <font name='Courier'>ValueError</font> terminates execution, "
            "preventing corrupted datasets from polluting downstream training. "
            "<br/>• <b>Model Serialization & Registration:</b> <font name='Courier'>src/train.py</font> fits the unified <font name='Courier'>ColumnTransformer</font> "
            "and <font name='Courier'>GradientBoostingClassifier</font>, serializing the resulting pipeline artifact to <font name='Courier'>models/pipeline.joblib</font> "
            "using atomic disk writes. "
            "<br/>• <b>Lifespan Model Loading (In-Memory Cache):</b> The FastAPI server (<font name='Courier'>src/api.py</font>) utilizes an asynchronous "
            "lifespan context manager to load <font name='Courier'>pipeline.joblib</font> into memory once at application startup. Subsequent HTTP requests "
            "execute inference directly against the in-memory pipeline, achieving sub-10ms response latencies. "
            "<br/>• <b>Client-Server REST Protocols:</b> The single-page frontend communicates with FastAPI over standard HTTP: "
            "<font name='Courier'>GET /metadata</font> returns JSON categories and cascading hierarchy trees; "
            "<font name='Courier'>POST /predict</font> accepts JSON payloads validated by Pydantic; and "
            "<font name='Courier'>POST /predict-batch</font> accepts multipart CSV file uploads and returns chunked CSV streams.",
            body,
        )
    )

    story.append(Paragraph("D. End-to-End Operational Execution Sequence", h2_style))
    story.append(
        Paragraph(
            "The complete operational lifecycle follows a rigorous, sequential data flow: "
            "<br/><b>Stage 1 (Ingestion):</b> Raw CSV loaded from <font name='Courier'>data/raw/elections.csv</font> with BOM sanitization. "
            "<br/><b>Stage 2 (Cleaning & Recovery):</b> 6 deterministic stages execute: whitespace stripping, type casting, party normalization, "
            "duplicate removal, physical outlier filtering, and grouped missingness backfilling. "
            "<br/><b>Stage 3 (Validation Barrier):</b> 6 automated assertions verify that row count >= 20k, duplicates == 0, voters > 0, "
            "seat density is between 1 and 100, categoricals are non-empty, and target is binary. Clean dataset saved to <font name='Courier'>data/cleaned/elections_cleaned.csv</font>. "
            "<br/><b>Stage 4 (Training & Serialization):</b> Post-poll leaking columns purged. Data split chronologically into Train (1970–2013) "
            "and Test (2018–2024). scikit-learn pipeline fitted and serialized to <font name='Courier'>models/pipeline.joblib</font>. "
            "<br/><b>Stage 5 (Backend Startup):</b> FastAPI boots on Uvicorn, pre-loads <font name='Courier'>pipeline.joblib</font> into RAM, "
            "and serves the interactive single-page application at <font name='Courier'>GET /</font>. "
            "<br/><b>Stage 6 (Client Discovery):</b> Browser executes <font name='Courier'>GET /metadata</font> to construct cascading dropdowns: "
            "selecting Province dynamically filters Macro Regions, which dynamically filters Electoral Zones. "
            "<br/><b>Stage 7 (Real-Time Inference):</b> User clicks 'Predict Seat Outcome'. Browser dispatches JSON to <font name='Courier'>POST /predict</font>. "
            "Pydantic validates fields, the in-memory pipeline predicts probabilities, and the UI animates the confidence gauge in sub-10ms.",
            body,
        )
    )

    story.append(PageBreak())
'''

with open('scratch/build_master_handbook.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('    # =========================================================================\n    # SECTION III: SYSTEM ARCHITECTURE')
end_idx = content.find('    # =========================================================================\n    # SECTION IV & V: REPOSITORY')

if start_idx != -1 and end_idx != -1:
    updated_content = content[:start_idx] + new_sec3 + content[end_idx:]
    with open('scratch/build_master_handbook.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print('Updated scratch/build_master_handbook.py successfully.')
else:
    print(f'Failed to find markers: start_idx={start_idx}, end_idx={end_idx}')
