# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Master IEEE Technical Report & Viva Voce Defense Guide for Pakistan Elections ML Pipeline."""

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PDF = PROJECT_ROOT / "docs" / "Pakistan_Elections_ML_Pipeline_Documentation.pdf"
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"
REPORTS_DIR = PROJECT_ROOT / "output" / "reports"


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas that accurately calculates total page numbers and renders IEEE-style running headers/footers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress running header/footer on cover/title page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))  # Slate 600

        # IEEE Running Top Header
        self.drawString(
            54,
            11 * 72 - 36,
            "IEEE TECHNICAL REPORT: PAKISTAN ELECTIONS ML PIPELINE (TRN-2026-000363)",
        )
        self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "QUDRAT ULLAH")

        # Top Dividing Rule
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Bottom Dividing Rule
        self.line(54, 44, 8.5 * 72 - 54, 44)

        # IEEE Running Bottom Footer
        self.setFont("Helvetica", 8)
        self.drawString(
            54, 32, "AtomCamp PSEB Fellowship | Data Engineering & Machine Learning Track"
        )
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 32, page_str)
        self.restoreState()


def make_callout(text, kind="note", width=504):
    """Generates an IEEE-styled visual callout box with a colored accent border."""
    palette = {
        "note": {
            "bg": colors.HexColor("#f8fafc"),
            "border": colors.HexColor("#0284c7"),
            "title": "NOTE",
            "title_col": colors.HexColor("#0369a1"),
        },
        "tip": {
            "bg": colors.HexColor("#f0fdf4"),
            "border": colors.HexColor("#16a34a"),
            "title": "PRO-TIP / BEST PRACTICE",
            "title_col": colors.HexColor("#15803d"),
        },
        "warning": {
            "bg": colors.HexColor("#fffbeb"),
            "border": colors.HexColor("#d97706"),
            "title": "CRITICAL WARNING / TRAP",
            "title_col": colors.HexColor("#b45309"),
        },
        "viva": {
            "bg": colors.HexColor("#faf5ff"),
            "border": colors.HexColor("#9333ea"),
            "title": "VIVA VOCE DEFENSE STRATEGY",
            "title_col": colors.HexColor("#7e22ce"),
        },
    }
    cfg = palette.get(kind, palette["note"])
    p_content = Paragraph(
        f"<b><font color='{cfg['title_col']}'>[{cfg['title']}]</font></b><br/>{text}",
        ParagraphStyle(
            "CalloutText",
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#1e293b"),
        ),
    )
    t = Table([[p_content]], colWidths=[width])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), cfg["bg"]),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("LINEBEFORE", (0, 0), (0, -1), 3.5, cfg["border"]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def build_handbook():
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#0f172a")    # Slate 900
    c_secondary = colors.HexColor("#0369a1")  # Blue 700
    c_emerald = colors.HexColor("#047857")    # Emerald 700
    c_text = colors.HexColor("#1e293b")       # Slate 800
    c_bg_light = colors.HexColor("#f8fafc")   # Slate 50
    c_border = colors.HexColor("#cbd5e1")     # Slate 300

    # IEEE Standard Typography Styles
    title_style = ParagraphStyle(
        "IEEETitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=25,
        textColor=c_primary,
        alignment=1,  # Centered
        spaceAfter=6,
    )

    author_style = ParagraphStyle(
        "IEEEAuthor",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        alignment=1,  # Centered
        spaceAfter=12,
    )

    abstract_style = ParagraphStyle(
        "IEEEAbstract",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=c_text,
        alignment=4,  # Justified
    )

    h1_style = ParagraphStyle(
        "IEEEH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=c_primary,
        spaceBefore=11,
        spaceAfter=4,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "IEEEH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.8,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
    )

    body = ParagraphStyle(
        "IEEEBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.6,
        leading=12.2,
        textColor=c_text,
        spaceAfter=5,
    )

    caption_style = ParagraphStyle(
        "IEEECaption",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#475569"),
        alignment=1,  # Centered
        spaceBefore=3,
        spaceAfter=5,
    )

    tbl_header = ParagraphStyle(
        "IEEETblHeader",
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10,
        textColor=colors.white,
        alignment=0,
    )

    tbl_text = ParagraphStyle(
        "IEEETblText",
        fontName="Helvetica",
        fontSize=7.6,
        leading=10.2,
        textColor=c_text,
    )

    tbl_mono = ParagraphStyle(
        "IEEETblMono",
        fontName="Courier",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0f172a"),
    )

    q_title_style = ParagraphStyle(
        "QTitle",
        fontName="Helvetica-Bold",
        fontSize=9.0,
        leading=12.0,
        textColor=c_primary,
    )

    q_ans_style = ParagraphStyle(
        "QAns",
        fontName="Helvetica",
        fontSize=8.4,
        leading=11.5,
        textColor=c_text,
    )

    story = []

    # =========================================================================
    # IEEE COVER & HEADER BLOCK
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            "<b>Pakistan Elections ML Pipeline: An End-to-End Data Engineering, "
            "Machine Learning and Interactive Serving Architecture</b>",
            title_style,
        )
    )
    story.append(
        Paragraph(
            "<b>Qudrat Ullah</b> (Trainee ID: TRN-2026-000363)<br/>"
            "<i>Data Engineering & Applied Machine Learning Track</i><br/>"
            "AtomCamp & Pakistan Software Export Board (PSEB) — November 20, 2026",
            author_style,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=8))

    # Abstract & Index Terms Box
    abstract_text = (
        "<b><i>Abstract</i>—This technical report documents the complete production implementation of the "
        "Pakistan Elections ML Pipeline. The system is engineered to solve a binary classification task: "
        "predicting whether a National Assembly candidate will win their constituency seat strictly prior to voting day. "
        "Using 54 years of official digitized Election Commission of Pakistan (ECP) gazettes (1970–2024, 24,585 records), "
        "the data engineering pipeline resolves UTF-8 BOM encoding anomalies, eliminates duplicate candidate entries, "
        "and handles 88.6% structural missingness in voter metrics via grouped constituency backfilling. "
        "To guarantee zero target leakage, all post-election metrics (actual votes, turnout percentages, and rejected ballots) "
        "are strictly purged. A scikit-learn ColumnTransformer and GradientBoostingClassifier pipeline is trained using "
        "a chronological split (1970–2013 train vs. 2018–2024 test), achieving a Precision-Recall AUC of 0.5958 (+440% over baseline) "
        "and an ROC-AUC of 0.8903. The model is served via a high-performance FastAPI backend with lifespan in-memory loading, "
        "dynamic cascading metadata dropdowns, batch CSV processing, and an interactive single-page application (SPA).</b><br/><br/>"
        "<b><i>Index Terms</i>—Data Engineering, Machine Learning, First-Past-The-Post, FastAPI, scikit-learn, "
        "Gradient Boosting, Target Leakage, Precision-Recall AUC, Concept Drift, Docker, Medallion Architecture.</b>"
    )
    t_abs = Table([[Paragraph(abstract_text, abstract_style)]], colWidths=[504])
    t_abs.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), c_bg_light),
                ("BOX", (0, 0), (-1, -1), 0.75, c_border),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(t_abs)
    story.append(Spacer(1, 8))

    # Table of Contents
    story.append(Paragraph("<b>Table of Contents (IEEE Sections)</b>", h2_style))
    toc_data = [
        [Paragraph("<b>I. Introduction & Operational Scope</b>", tbl_text), Paragraph("Problem formulation, pre-election scope, user personas & non-goals", tbl_text)],
        [Paragraph("<b>II. Related Data & Raw Gazette Audit</b>", tbl_text), Paragraph("Raw gazette defects, UTF-8 BOM bug, 88.6% null recovery & 14-column schema", tbl_text)],
        [Paragraph("<b>III. System Architecture & Workflows</b>", tbl_text), Paragraph("9-component topology, medallion data flow & operational workflows", tbl_text)],
        [Paragraph("<b>IV. Repository Structure & Immutability</b>", tbl_text), Paragraph("Directory tree, component mapping & raw folder protection rules", tbl_text)],
        [Paragraph("<b>V. Python Codebase Deep Dive</b>", tbl_text), Paragraph("Module-by-module analysis: config, clean, validate, train, predict, api", tbl_text)],
        [Paragraph("<b>VI. Machine Learning Engine & Math</b>", tbl_text), Paragraph("Leakage firewall, temporal split justification, GradientBoosting & PR-AUC math", tbl_text)],
        [Paragraph("<b>VII. Design Decisions & Trade-Offs</b>", tbl_text), Paragraph("Architectural decisions matrix: chosen paths vs. discarded alternatives", tbl_text)],
        [Paragraph("<b>VIII. Quality Gate & Reproducibility</b>", tbl_text), Paragraph("Automated validation, pytest suite & zero-drift random seed controls", tbl_text)],
        [Paragraph("<b>IX. Visual Analytics, UI & Experiments</b>", tbl_text), Paragraph("Exhaustive analysis of all 8 figures, including live UI screenshot & prediction example", tbl_text)],
        [Paragraph("<b>X. Model Governance & Limitations</b>", tbl_text), Paragraph("Formal Model Card, fair use ethical boundaries & 2024 independent drift", tbl_text)],
        [Paragraph("<b>XI. Operational Runbook & Commands</b>", tbl_text), Paragraph("Step-by-step CLI commands, flags, expected outputs & Docker deployment", tbl_text)],
        [Paragraph("<b>XII. Technical Glossary (25 Terms)</b>", tbl_text), Paragraph("Jargon-free definitions of core data engineering and ML concepts", tbl_text)],
        [Paragraph("<b>XIII. Master Viva Voce Defense Q&A</b>", tbl_text), Paragraph("25 rigorous technical defense questions and model oral answers", tbl_text)],
        [Paragraph("<b>XIV. Open Questions & Honest Reconciliation</b>", tbl_text), Paragraph("Delimitation boundaries, multi-seat candidacies & honest research notes", tbl_text)],
    ]
    t_toc = Table(toc_data, colWidths=[175, 329])
    t_toc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.75, c_border),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(t_toc)

    story.append(PageBreak())

    # =========================================================================
    # SECTION I: INTRODUCTION & OPERATIONAL SCOPE
    # =========================================================================
    story.append(Paragraph("I. Introduction & Operational Scope", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    story.append(Paragraph("A. Problem Formulation and Pre-Election Value", h2_style))
    story.append(
        Paragraph(
            "The <b>Pakistan Elections ML Pipeline</b> is an end-to-end data engineering and predictive machine learning system. "
            "Its mission is to evaluate a candidate's likelihood of winning a National Assembly constituency seat in Pakistan "
            "<b>strictly prior to voting day</b>. "
            "In predictive modeling, pre-election classification means utilizing only structural, institutional, and geographic parameters "
            "that are fixed and verifiable before polls open (such as the candidate's political party, the province, macro-region, "
            "electoral zone, total registered voters, and the number of contesting opponents).",
            body,
        )
    )

    story.append(Paragraph("B. Target Stakeholder Personas", h2_style))
    story.append(
        Paragraph(
            "The system is designed with three distinct stakeholder personas: "
            "<br/>• <b>Political & Electoral Analysts:</b> Utilize the interactive web simulator to conduct 'what-if' seat simulation, "
            "evaluating how a split ticket or a crowded field of independent candidates shifts a major party's winning probability. "
            "<br/>• <b>Data Science Assessors & Teaching Assistants:</b> Inspect the rigor of the data cleaning pipeline, "
            "confirm that no post-election target leakage exists, and verify 100% test suite execution via <font name='Courier'>pytest</font>. "
            "<br/>• <b>Campaign Data Teams:</b> Submit bulk nomination rosters via the batch CSV prediction endpoint to score entire "
            "provinces simultaneously, downloading calibrated probability reports for strategic campaign resource allocation.",
            body,
        )
    )

    story.append(Paragraph("C. Operational Non-Goals", h2_style))
    story.append(
        Paragraph(
            "Professional engineering documentation must explicitly define the system's operational boundaries: "
            "<br/>1. <b>Not an Exit Poll or Vote Counter:</b> The model does not count ballots, project voter turnout on election night, "
            "or process electronic voting machine totals. "
            "<br/>2. <b>Not a National Majority Coalition Simulator:</b> The model evaluates individual seat contests independently; "
            "it does not predict prime ministerial floor votes or post-poll parliamentary coalition negotiations. "
            "<br/>3. <b>Not a Micro-Targeting Voter Engine:</b> The system operates entirely at the constituency and candidate level; "
            "it does not track individual citizen voting histories or demographic census micro-data.",
            body,
        )
    )

    story.append(
        make_callout(
            "<b>Key Boundary:</b> The model deliberately excludes candidate personal names and individual campaign spend. "
            "Personal names are high-cardinality strings that cause memorization without generalization. "
            "The system measures the structural strength of the party ticket within the historical political geography.",
            kind="note",
        )
    )

    # =========================================================================
    # SECTION II: DATA ENGINEERING & RAW GAZETTE AUDIT
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("II. Related Data & Raw Gazette Audit", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    story.append(Paragraph("A. Historical Corpus (1970–2024)", h2_style))
    story.append(
        Paragraph(
            "The raw dataset is stored at <font name='Courier'>data/raw/elections.csv</font>. "
            "It compiles 24,585 candidate records spanning 11 general elections: 1970, 1977, 1988, 1990, 1993, 1997, 2002, 2008, 2013, 2018, and 2024. "
            "This historical corpus represents official Election Commission of Pakistan (ECP) gazette returns digitized across five decades.",
            body,
        )
    )

    story.append(Paragraph("B. Deep Dive: Gazette Flaws and Sanitization", h2_style))
    story.append(
        Paragraph(
            "Decades of manual administrative gazette entry created severe data anomalies. "
            "Our data engineering pipeline isolates and repairs four critical failure modes: "
            "<br/>1. <b>The Byte Order Mark (BOM) Anomaly:</b> The raw CSV was encoded with a UTF-8 BOM prefix (<font name='Courier'>\\ufeff</font>). "
            "Standard readers treat this byte sequence as part of the first column name, yielding <font name='Courier'>'\\ufeffYear'</font> instead of <font name='Courier'>'Year'</font>, "
            "crashing downstream schema lookups. Loading with <font name='Courier'>encoding='utf-8-sig'</font> safely strips the byte sequence. "
            "<br/>2. <b>Structural Gazette Missingness (88.6% Nulls):</b> In official election printing, constituency-level metrics "
            "(<font name='Courier'>Registered Voters</font>, <font name='Courier'>Rejected Votes</font>, and <font name='Courier'>Turnout N</font>) "
            "were recorded only once per seat—typically on the winning candidate's row. All runner-up candidates had these fields left blank (<font name='Courier'>NaN</font>). "
            "Dropping rows with nulls would have destroyed 88.6% of the historical record! The pipeline resolves this by grouping by <font name='Courier'>['Year', 'Constituency']</font> "
            "and executing <font name='Courier'>transform('first')</font> to carry constituency-level figures down across all contestants. "
            "<br/>3. <b>Impossible Physical Values:</b> Raw gazettes contained negative vote totals, turnout values exceeding 100%, and candidate vote counts "
            "that were larger than the total registered voters in the district. These physical impossibilities are converted to <font name='Courier'>NaN</font> using vectorized NumPy conditions. "
            "<br/>4. <b>Duplicate Row Artifacts:</b> In 2024 data, partial-null duplicate records existed where an identical candidate entry appeared twice—one with voter totals and one without. "
            "Sorting by non-null voter counts preserves the complete gazette entry and eliminates 66 partial copies.",
            body,
        )
    )

    story.append(Paragraph("TABLE I: EXHAUSTIVE 14-COLUMN CLEAN DATASET SCHEMA", caption_style))
    schema_full = [
        [Paragraph("Column Name", tbl_header), Paragraph("Dtype", tbl_header), Paragraph("Description & Meaning", tbl_header), Paragraph("Allowed Range / Domain", tbl_header)],
        [Paragraph("Year", tbl_mono), Paragraph("int64", tbl_mono), Paragraph("Election calendar year", tbl_text), Paragraph("{1970, 1977, 1988, 1990, 1993, 1997, 2002, 2008, 2013, 2018, 2024}", tbl_text)],
        [Paragraph("Constituency", tbl_mono), Paragraph("string", tbl_mono), Paragraph("Full seat name with prefix", tbl_text), Paragraph("e.g., 'NA-1 Peshawar-I', 'NA-120 Lahore'", tbl_text)],
        [Paragraph("Candidate Name", tbl_mono), Paragraph("string", tbl_mono), Paragraph("Contesting individual name", tbl_text), Paragraph("Exempt from modeling (avoids memorization)", tbl_text)],
        [Paragraph("Party", tbl_mono), Paragraph("string", tbl_mono), Paragraph("Standardized party acronym", tbl_text), Paragraph("PTI, PML-N, PPP, IND, JUI-F, MQM, JI, etc.", tbl_text)],
        [Paragraph("Votes", tbl_mono), Paragraph("float64", tbl_mono), Paragraph("Actual ballot count received", tbl_text), Paragraph(">= 0 (Strictly dropped during training)", tbl_text)],
        [Paragraph("Valid Votes", tbl_mono), Paragraph("float64", tbl_mono), Paragraph("Total valid ballots in seat", tbl_text), Paragraph("Sum of all candidate votes in seat", tbl_text)],
        [Paragraph("Rejected Votes", tbl_mono), Paragraph("float64", tbl_mono), Paragraph("Invalid/spoiled ballot count", tbl_text), Paragraph(">= 0 (Strictly dropped during training)", tbl_text)],
        [Paragraph("Total Votes", tbl_mono), Paragraph("float64", tbl_mono), Paragraph("Total ballots cast (Valid+Rejected)", tbl_text), Paragraph("Total Votes <= Registered Voters", tbl_text)],
        [Paragraph("Registered Voters", tbl_mono), Paragraph("float64", tbl_mono), Paragraph("Eligible registered citizens", tbl_text), Paragraph("Range: 50,000 to 10,000,000", tbl_text)],
        [Paragraph("Province", tbl_mono), Paragraph("string", tbl_mono), Paragraph("Administrative province", tbl_text), Paragraph("Punjab, Sindh, KPK, Balochistan, ICT", tbl_text)],
        [Paragraph("Regions 5", tbl_mono), Paragraph("string", tbl_mono), Paragraph("Macro geographic division", tbl_text), Paragraph("KPK, Karachi, Interior Sindh, Balochistan, Other", tbl_text)],
        [Paragraph("Zones 20", tbl_mono), Paragraph("string", tbl_mono), Paragraph("Electoral cluster zone", tbl_text), Paragraph("20 administrative zones across Pakistan", tbl_text)],
        [Paragraph("Six Parties", tbl_mono), Paragraph("string", tbl_mono), Paragraph("Historical political bloc", tbl_text), Paragraph("PTI, PML (s)/IJI, PPP (s)/PDA, Religious, etc.", tbl_text)],
        [Paragraph("num_candidates_in_seat", tbl_mono), Paragraph("int64", tbl_mono), Paragraph("Seat crowdedness metric", tbl_text), Paragraph("Count of candidates in seat (1 to 100)", tbl_text)],
        [Paragraph("is_winner", tbl_mono), Paragraph("int64", tbl_mono), Paragraph("Binary target variable", tbl_text), Paragraph("1 = Seat Winner, 0 = Runner-Up", tbl_text)],
    ]
    t_sch = Table(schema_full, colWidths=[110, 48, 166, 180])
    t_sch.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), c_primary),
                ("BOX", (0, 0), (-1, -1), 1, c_border),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("TOPPADDING", (0, 0), (-1, -1), 2.0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ]
        )
    )
    story.append(t_sch)

    story.append(PageBreak())

    # =========================================================================
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
    # =========================================================================
    # SECTION IV & V: REPOSITORY & CODEBASE DEEP DIVE
    # =========================================================================
    story.append(Paragraph("IV. Repository Structure & Directory Anatomy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    tree_text = (
        "pakistan-elections-ml-pipeline/\n"
        "├── .github/workflows/ci.yml       # Automated GitHub Actions test execution\n"
        "├── data/\n"
        "│   ├── raw/                       # Immutable raw gazette CSV (24,585 rows)\n"
        "│   └── cleaned/                   # elections_cleaned.csv (24,324 rows passing quality gate)\n"
        "├── docs/                          # Architectural documentation & PDF handbook\n"
        "├── frontend/index.html            # Zero-dependency HTML5/CSS3/Vanilla JS UI\n"
        "├── models/pipeline.joblib         # Serialized Gradient Boosting pipeline\n"
        "├── output/\n"
        "│   ├── figures/                   # Turnout, confusion matrix, feature importance PNGs\n"
        "│   └── reports/                   # metrics.json, model_comparison.csv, error audits\n"
        "├── src/\n"
        "│   ├── config.py                  # Central paths, feature lists, hyperparameters\n"
        "│   ├── load_data.py               # UTF-8 BOM-aware CSV loading functions\n"
        "│   ├── cleaning.py                # 6 deterministic cleaning & recovery stages\n"
        "│   ├── validation.py              # Automated 6-check Quality Gate\n"
        "│   ├── train.py                   # Temporal split, ColumnTransformer & model training\n"
        "│   ├── predict.py                 # CLI batch prediction scoring script\n"
        "│   └── api.py                     # Production FastAPI server & REST endpoints\n"
        "├── tests/\n"
        "│   ├── test_cleaning.py           # Unit tests for data cleaning & quality gate\n"
        "│   └── test_api.py                # Integration tests for FastAPI endpoints & validation\n"
        "├── Dockerfile                     # Multi-stage production container definition\n"
        "├── requirements.txt               # Pinned Python package dependencies\n"
        "└── README.md                      # Operational guide, setup commands & API specs"
    )
    story.append(
        Paragraph(
            f"<font name='Courier' size='7'>{tree_text.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>",
            body,
        )
    )

    story.append(Paragraph("A. Raw Folder Protection Rules", h2_style))
    story.append(
        Paragraph(
            "In professional data engineering, the raw data directory (<font name='Courier'>data/raw/</font>) is treated as read-only. "
            "No script, cleaning function, or engineer may ever modify or overwrite files in this folder. "
            "Treating raw data as an immutable event log guarantees reproducibility: if a bug is identified in a cleaning rule, "
            "the pipeline can be completely re-run from scratch without data loss.",
            body,
        )
    )

    story.append(Spacer(1, 4))
    story.append(Paragraph("V. Python Codebase Deep Dive", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    py_modules = [
        ("src/config.py", "Centralized Configuration & Constants",
         "Defines all filesystem paths, the 7 feature column names, leakage columns, and random seed (42). "
         "Centralizing configuration prevents hardcoded string drift across disparate modules."),
        ("src/load_data.py", "Safe Gazette Data Ingestion",
         "Wraps pandas CSV loading with explicit encoding handling (<font name='Courier'>utf-8-sig</font>). "
         "Eliminates the silent UTF-8 BOM bug that corrupts the first column header."),
        ("src/cleaning.py", "Deterministic Data Sanitization & Recovery",
         "Implements 6 pure transformation functions: text stripping, numeric type conversion, party alias normalization, "
         "exact deduplication, physical outlier removal, and grouped missingness backfill. "
         "Transforms 24,585 raw rows into 24,324 high-integrity records."),
        ("src/validation.py", "Automated Quality Gate",
         "Asserts 6 non-negotiable data integrity checks before model training. "
         "Halts the pipeline with an explicit exception if row count drops below 20,000 or duplicate rows exist."),
        ("src/train.py", "Model Training & Pipeline Serialization",
         "Partitions data chronologically (1970–2013 train vs. 2018–2024 test). Constructs a scikit-learn "
         "<font name='Courier'>ColumnTransformer</font> and trains a <font name='Courier'>GradientBoostingClassifier</font>. "
         "Saves the fitted pipeline to <font name='Courier'>models/pipeline.joblib</font>."),
        ("src/predict.py", "Batch Scoring Engine",
         "CLI utility that accepts an arbitrary candidate CSV, validates required features, "
         "applies the saved pipeline, and outputs an annotated CSV with win probabilities."),
        ("src/api.py", "Production FastAPI REST Service",
         "Production ASGI backend. Uses lifespan management to load <font name='Courier'>pipeline.joblib</font> once at startup. "
         "Exposes <font name='Courier'>GET /</font>, <font name='Courier'>GET /health</font>, <font name='Courier'>GET /metadata</font>, "
         "<font name='Courier'>POST /predict</font>, and <font name='Courier'>POST /predict-batch</font>."),
        ("tests/test_cleaning.py & test_api.py", "Automated Test Harness",
         "14 exhaustive unit and integration tests executed via <font name='Courier'>pytest</font>. "
         "Verifies every cleaning function, the quality gate, schema validation errors, and API endpoints."),
    ]
    for mod_path, mod_name, mod_desc in py_modules:
        story.append(Paragraph(f"<b>{mod_path}</b>: {mod_name}", h2_style))
        story.append(Paragraph(mod_desc, body))

    story.append(PageBreak())

    # =========================================================================
    # SECTION VI & VII: ML FOUNDATIONS & DESIGN DECISIONS
    # =========================================================================
    story.append(Paragraph("VI. Machine Learning Engine & Anti-Leakage Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    story.append(Paragraph("A. Target Formulation and Modeling Value", h2_style))
    story.append(
        Paragraph(
            "The model target is <font name='Courier'>is_winner</font> (1 = candidate won the seat, 0 = candidate lost). "
            "In Pakistan's First-Past-The-Post (FPTP) system, each National Assembly constituency elects exactly one winner. "
            "Predicting this outcome prior to polling day provides immense value to political strategists and researchers, "
            "allowing objective identification of contested battleground seats versus safe party strongholds.",
            body,
        )
    )

    story.append(Paragraph("B. Target Leakage Firewall", h2_style))
    story.append(
        Paragraph(
            "Target leakage occurs when a model is trained on features that are only generated <i>after</i> the target event has occurred. "
            "Including post-election metrics produces artificially inflated training scores that collapse in real-world deployment. "
            "The pipeline enforces a strict leakage firewall, permanently dropping six columns: "
            "<br/>• <font name='Courier'>Votes</font>: The actual number of votes cast for the candidate on election day. "
            "<br/>• <font name='Courier'>vote_share_pct</font>: The candidate's final percentage of valid votes. "
            "<br/>• <font name='Courier'>log_votes</font>: The mathematical log transformation of the final vote tally. "
            "<br/>• <font name='Courier'>Turnout N</font>: The total voter turnout percentage recorded when polls close. "
            "<br/>• <font name='Courier'>Rejected Votes</font>: The count of disqualified ballots tallied during official counting. "
            "<br/>• <font name='Courier'>Candidate Name</font>: High-cardinality personal identifiers dropped to avoid memorization.",
            body,
        )
    )

    story.append(Paragraph("C. Temporal Train/Test Split Justification", h2_style))
    story.append(
        Paragraph(
            "A standard random k-fold train/test split randomly scrambles rows across all election years. "
            "In electoral forecasting, random splitting causes <b>temporal data leakage</b>: the model might train on 2024 results to predict a 1993 contest! "
            "To simulate genuine future prediction, we enforce a strict <b>chronological split</b>: "
            "<br/>• <b>Training Set (1970–2013):</b> 15,879 candidate records across 9 general elections. "
            "<br/>• <b>Held-Out Test Set (2018–2024):</b> 8,445 candidate records across the two most recent general elections.",
            body,
        )
    )

    story.append(Paragraph("VII. Architectural Decisions & Trade-Offs Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))
    story.append(Paragraph("TABLE II: ARCHITECTURAL DECISIONS AND TRADE-OFFS", caption_style))

    decisions = [
        [Paragraph("Engineering Decision", tbl_header), Paragraph("Alternatives Considered", tbl_header), Paragraph("Why This Path Was Chosen", tbl_header), Paragraph("Trade-Off & Cost", tbl_header)],
        [Paragraph("CSV File Storage", tbl_text), Paragraph("PostgreSQL / SQLite", tbl_text), Paragraph("Zero operational overhead; versionable via Git", tbl_text), Paragraph("Lacks ACID transactions for high concurrency", tbl_text)],
        [Paragraph("Temporal Split (1970-2013 / 2018-2024)", tbl_text), Paragraph("Random 80/20 train/test split", tbl_text), Paragraph("Prevents temporal leakage; simulates real-world future prediction", tbl_text), Paragraph("Test set reflects concept drift from recent political events", tbl_text)],
        [Paragraph("Grouped Missingness Propagation", tbl_text), Paragraph("Drop rows with nulls", tbl_text), Paragraph("Preserves 88.6% of historical rows by backfilling district totals", tbl_text), Paragraph("Assumes gazette first-row figures apply to entire seat", tbl_text)],
        [Paragraph("Gradient Boosting Classifier", tbl_text), Paragraph("Logistic Regression, Random Forest", tbl_text), Paragraph("Superior non-linear boundary capture; handles class imbalance", tbl_text), Paragraph("Longer training time; complex hyperparameter tuning", tbl_text)],
        [Paragraph("PR-AUC Primary Evaluation Metric", tbl_text), Paragraph("Accuracy, ROC-AUC", tbl_text), Paragraph("Accurately measures positive class detection under 1:8 imbalance", tbl_text), Paragraph("Less intuitive to non-technical stakeholders than accuracy", tbl_text)],
        [Paragraph("scikit-learn ColumnTransformer", tbl_text), Paragraph("Manual pandas script preprocessing", tbl_text), Paragraph("Atomic serialization; guarantees identical feature encoding in API", tbl_text), Paragraph("Inference requires rigid DataFrame schema match", tbl_text)],
    ]
    t_dec = Table(decisions, colWidths=[95, 105, 160, 144])
    t_dec.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), c_primary),
                ("BOX", (0, 0), (-1, -1), 1, c_border),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ]
        )
    )
    story.append(t_dec)

    story.append(PageBreak())

    # =========================================================================
    # SECTION VIII: QUALITY ASSURANCE & REPRODUCIBILITY
    # =========================================================================
    story.append(Paragraph("VIII. Data Quality Assurance & Reproducibility", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    story.append(Paragraph("A. The 6-Check Automated Quality Gate", h2_style))
    story.append(
        Paragraph(
            "Before clean data is exported or consumed by model training, <font name='Courier'>src/validation.py</font> "
            "executes a strict quality gate enforcing six mandatory checks: "
            "<br/>1. <b>Row Count Integrity:</b> Total cleaned rows must be >= 20,000 (actual: 24,324). "
            "<br/>2. <b>Zero Exact Duplicates:</b> Identical candidate duplicate rows must be exactly zero. "
            "<br/>3. <b>Physical Voter Validity:</b> Registered voters must be strictly positive (> 0). "
            "<br/>4. <b>Constituency Crowdedness Bounds:</b> Contesting candidates per seat must be between 1 and 100. "
            "<br/>5. <b>Categorical Completeness:</b> Required categoricals (<font name='Courier'>Province</font>, <font name='Courier'>Party</font>) must have zero blanks. "
            "<br/>6. <b>Binary Target Integrity:</b> Target variable <font name='Courier'>is_winner</font> must contain only values in {0, 1}.",
            body,
        )
    )

    story.append(Paragraph("B. Test Suite Execution", h2_style))
    story.append(
        Paragraph(
            "The repository includes 14 automated tests executed with <font name='Courier'>pytest</font>. "
            "The tests span both data engineering and REST serving layers: "
            "<br/>• <font name='Courier'>tests/test_cleaning.py</font> (7 tests): Validates whitespace stripping, numeric typing, "
            "party standardization, duplicate elimination, outlier filtering, grouped missingness, and quality gate enforcement. "
            "<br/>• <font name='Courier'>tests/test_api.py</font> (7 tests): Verifies <font name='Courier'>GET /health</font>, "
            "<font name='Courier'>GET /metadata</font> cascading hierarchy, single candidate prediction validation, HTTP 422 error trapping, "
            "and batch CSV upload scoring.",
            body,
        )
    )

    story.append(Paragraph("C. Exact Reproducibility Controls", h2_style))
    story.append(
        Paragraph(
            "Machine learning experiments are only credible if they produce bit-for-bit identical results on every run. "
            "The pipeline achieves deterministic reproducibility through three core mechanisms: "
            "<br/>1. <b>Fixed Random Seed:</b> Global seed <font name='Courier'>RANDOM_STATE = 42</font> pinned across scikit-learn estimators. "
            "<br/>2. <b>Pinned Dependencies:</b> Exact package versions frozen in <font name='Courier'>requirements.txt</font>. "
            "<br/>3. <b>Atomic Artifact Serialization:</b> Preprocessing encoders and gradient boosting trees are serialized together "
            "into a single <font name='Courier'>models/pipeline.joblib</font> file, preventing preprocessing mismatch between training and inference.",
            body,
        )
    )

    # =========================================================================
    # SECTION IX: VISUAL ANALYTICS, UI & EXPERIMENTAL RESULTS
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("IX. Visual Analytics, UI Simulator & Experimental Results", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    story.append(
        Paragraph(
            "This section provides an exhaustive visual walkthrough of all eight graphical artifacts generated across "
            "exploratory data analysis, model diagnostics, error auditing, and the interactive web simulator interface. "
            "Each figure is paired with an in-depth explanation of its axes, data patterns, data engineering importance, "
            "and viva voce defense relevance.",
            body,
        )
    )

    # Figure 2: Turnout by Year
    if (FIGURES_DIR / "01_turnout_by_year.png").exists():
        story.append(KeepTogether([
            Image(str(FIGURES_DIR / "01_turnout_by_year.png"), width=5.6 * inch, height=2.9 * inch),
            Spacer(1, 2),
            Paragraph("<b>Fig. 2.</b> Voter Turnout Trend in Pakistan General Elections (1970–2024).", caption_style)
        ]))
        story.append(
            Paragraph(
                "<b>Detailed Interpretation:</b> "
                "<br/>• <b>Axes & Elements:</b> X-axis tracks election years; Y-axis measures aggregate voter turnout percentage. "
                "<br/>• <b>Historical Trends:</b> Turnout peaked at ~63% in 1970, dropped to ~35% in 1997, rose to 55% in 2013, and stabilized near 48% in 2024. "
                "<br/>• <b>Data Engineering Lesson:</b> Voter turnout is only known <i>after</i> voting day. Including turnout as an input feature would constitute "
                "catastrophic target leakage. The model deliberately relies only on pre-election structural voter registration figures.",
                body,
            )
        )

    story.append(PageBreak())

    # Figure 3: Top Parties 2024 Votes
    if (FIGURES_DIR / "02_top_parties_2024_votes.png").exists():
        story.append(KeepTogether([
            Image(str(FIGURES_DIR / "02_top_parties_2024_votes.png"), width=5.6 * inch, height=3.0 * inch),
            Spacer(1, 2),
            Paragraph("<b>Fig. 3.</b> Top Political Parties by Total Popular Vote in the 2024 General Election.", caption_style)
        ]))
        story.append(
            Paragraph(
                "<b>Detailed Interpretation:</b> "
                "<br/>• <b>Distribution:</b> Demonstrates the tri-partite dominance of PML-N, Independent candidates (including PTI-backed nominees), "
                "and PPP, followed by TLP, JUI-F, and MQM-P. "
                "<br/>• <b>Concept Drift Lesson:</b> The massive vote share of 'Independent' candidates in 2024 represents an acute concept drift event, "
                "caused by the legal loss of PTI's electoral symbol.",
                body,
            )
        )

    # Figure 4: Log Votes Distribution
    if (FIGURES_DIR / "03_log_votes_distribution.png").exists():
        story.append(KeepTogether([
            Image(str(FIGURES_DIR / "03_log_votes_distribution.png"), width=5.6 * inch, height=2.9 * inch),
            Spacer(1, 2),
            Paragraph("<b>Fig. 4.</b> Distribution of Raw Votes (Skewed) vs. Log-Transformed Votes (Normalized).", caption_style)
        ]))
        story.append(
            Paragraph(
                "<b>Detailed Interpretation:</b> "
                "<br/>• <b>Statistical Shape:</b> Raw votes are heavily right-skewed (80% receive <5k votes; winners receive 70k–130k+). "
                "Log transformation normalizes this into a bell curve. Both columns are purged from training features to avoid target leakage.",
                body,
            )
        )

    story.append(PageBreak())

    # Figure 5: Confusion Matrix
    if (FIGURES_DIR / "04_confusion_matrix.png").exists():
        story.append(KeepTogether([
            Image(str(FIGURES_DIR / "04_confusion_matrix.png"), width=4.3 * inch, height=3.4 * inch),
            Spacer(1, 2),
            Paragraph("<b>Fig. 5.</b> Out-of-Time Test Set Confusion Matrix (2018–2024 General Elections).", caption_style)
        ]))
        story.append(
            Paragraph(
                "<b>Detailed Interpretation:</b> "
                "<br/>• <b>Exact Breakdown:</b> True Negatives (7,169 non-winners correctly predicted), True Positives (411 winners correctly predicted). "
                "<br/>• <b>Class Imbalance:</b> In a 1:8 imbalanced problem, PR-AUC of 0.5958 represents a 440% improvement over random guessing (~0.11).",
                body,
            )
        )

    # Figure 6: Permutation Feature Importance
    if (FIGURES_DIR / "06_feature_importance.png").exists():
        story.append(KeepTogether([
            Image(str(FIGURES_DIR / "06_feature_importance.png"), width=5.6 * inch, height=3.0 * inch),
            Spacer(1, 2),
            Paragraph("<b>Fig. 6.</b> Permutation Feature Importance on Held-Out Test Set (Mean Drop in PR-AUC).", caption_style)
        ]))
        story.append(
            Paragraph(
                "<b>Detailed Interpretation:</b> "
                "<br/>• <b>Dominant Features:</b> Political party affiliation (<font name='Courier'>Party</font>) is overwhelmingly the #1 predictor "
                "(~0.14 drop), followed by seat crowdedness (<font name='Courier'>num_candidates_in_seat</font>) and registered voter volume.",
                body,
            )
        )

    story.append(PageBreak())

    # Figure 7: Error Rate by Province
    if (FIGURES_DIR / "07_error_rate_by_province.png").exists():
        story.append(KeepTogether([
            Image(str(FIGURES_DIR / "07_error_rate_by_province.png"), width=5.6 * inch, height=2.9 * inch),
            Spacer(1, 2),
            Paragraph("<b>Fig. 7.</b> Model Classification Error Rate Breakdown Across Administrative Provinces.", caption_style)
        ]))
        story.append(
            Paragraph(
                "<b>Detailed Interpretation:</b> "
                "<br/>• <b>Regional Error:</b> Punjab (~8.5%), ICT (~9.1%), Sindh (~10.2%), KPK (~11.4%), and Balochistan (~16.8%). "
                "Balochistan has the highest error due to low voter density, vast geography, and candidate fragmentation across 20+ contestants.",
                body,
            )
        )

    # Figure 8: Live UI Screenshot & Example Walkthrough
    if (FIGURES_DIR / "08_ui_screenshot.png").exists():
        story.append(KeepTogether([
            Image(str(FIGURES_DIR / "08_ui_screenshot.png"), width=6.6 * inch, height=4.1 * inch),
            Spacer(1, 2),
            Paragraph("<b>Fig. 8.</b> Interactive Candidate Feature Simulator UI with Lahore Example Prediction.", caption_style)
        ]))
        story.append(
            Paragraph(
                "<b>Step-by-Step UI Inference Example Walkthrough:</b> "
                "<br/>• <b>Concrete Example Scenario:</b> The analyst evaluates a candidate contesting from <b>NA-120 Lahore</b>: "
                "<br/>  - <i>Province:</i> Punjab (selected from cascading parent dropdown) "
                "<br/>  - <i>Macro Region (5):</i> All other Territories (dynamically filtered for Punjab) "
                "<br/>  - <i>Electoral Zone (20):</i> Zone-5 (Central -2) Lahore Division "
                "<br/>  - <i>Political Party:</i> PML-N (auto-syncs Six Parties bloc to 'PML (s)/IJI/PNA') "
                "<br/>  - <i>Registered Voters:</i> 350,000 | <i>Contesting Candidates:</i> 14 "
                "<br/>• <b>Inference Result:</b> Clicking <b>'Predict Seat Outcome'</b> executes inference in sub-10ms: "
                "<br/>  - <b>Predicted Winner: 1 (Likely Winner)</b> "
                "<br/>  - <b>Win Probability: 78.45%</b> (illustrated with an animated green progress bar) "
                "<br/>• <b>Why This Outcome Makes Sense:</b> PML-N in urban Lahore has a commanding historical win rate. "
                "Even with 14 candidates diluting votes, the party machinery establishes a decisive winning threshold.",
                body,
            )
        )

    # Summary Metrics Table
    story.append(Spacer(1, 4))
    story.append(Paragraph("TABLE III: FINAL TEST SET PERFORMANCE BENCHMARK", caption_style))
    metrics_summary = [
        [Paragraph("Evaluation Metric", tbl_header), Paragraph("Score", tbl_header), Paragraph("Random Baseline", tbl_header), Paragraph("Engineering Assessment", tbl_header)],
        [Paragraph("PR-AUC (Precision-Recall)", tbl_mono), Paragraph("0.5958", tbl_mono), Paragraph("~0.1100", tbl_mono), Paragraph("Primary metric: +440% improvement over random guess", tbl_text)],
        [Paragraph("ROC-AUC (Discrimination)", tbl_mono), Paragraph("0.8903", tbl_mono), Paragraph("0.5000", tbl_mono), Paragraph("Near 0.90: Outstanding rank-ordering capability", tbl_text)],
        [Paragraph("Overall Accuracy", tbl_mono), Paragraph("89.70%", tbl_mono), Paragraph("88.80%", tbl_mono), Paragraph("High baseline due to 1:8 class ratio", tbl_text)],
        [Paragraph("Macro F1-Score", tbl_mono), Paragraph("0.7020", tbl_mono), Paragraph("0.4700", tbl_mono), Paragraph("Strong balanced harmonic mean across classes", tbl_text)],
    ]
    t_met = Table(metrics_summary, colWidths=[120, 55, 80, 249])
    t_met.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), c_primary),
                ("BOX", (0, 0), (-1, -1), 1, c_border),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ]
        )
    )
    story.append(t_met)

    story.append(PageBreak())

    # =========================================================================
    # SECTION X: GOVERNANCE, RISKS & MODEL CARD
    # =========================================================================
    story.append(Paragraph("X. Model Governance & Limitations", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))
    story.append(Paragraph("TABLE IV: FORMAL MACHINE LEARNING MODEL CARD", caption_style))

    mcard = [
        [Paragraph("Model Card Field", tbl_header), Paragraph("Specification & Detail", tbl_header)],
        [Paragraph("Model Architecture", tbl_text), Paragraph("GradientBoostingClassifier (100 estimators, max_depth=3, lr=0.1) wrapped in ColumnTransformer", tbl_text)],
        [Paragraph("Primary Intended Task", tbl_text), Paragraph("Pre-election binary classification of seat winner likelihood (is_winner in {0, 1})", tbl_text)],
        [Paragraph("Target Users", tbl_text), Paragraph("Political analysts, electoral researchers, campaign planning data teams", tbl_text)],
        [Paragraph("Input Features (7)", tbl_text), Paragraph("Registered Voters, num_candidates_in_seat, Province, Regions 5, Zones 20, Party, Six Parties", tbl_text)],
        [Paragraph("Training Dataset", tbl_text), Paragraph("15,879 candidate records spanning 1970 to 2013 general elections (9 elections)", tbl_text)],
        [Paragraph("Evaluation Dataset", tbl_text), Paragraph("8,445 candidate records spanning 2018 and 2024 general elections (held-out test set)", tbl_text)],
        [Paragraph("Performance Metrics", tbl_text), Paragraph("PR-AUC: 0.5958 | ROC-AUC: 0.8903 | Accuracy: 89.70% | Macro F1: 0.7020", tbl_text)],
        [Paragraph("Primary Known Limitation", tbl_text), Paragraph("Vulnerable to sudden institutional symbol bans (e.g., 2024 PTI-backed independents)", tbl_text)],
    ]
    t_mc = Table(mcard, colWidths=[130, 374])
    t_mc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), c_primary),
                ("BOX", (0, 0), (-1, -1), 1, c_border),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, c_bg_light]),
            ]
        )
    )
    story.append(t_mc)

    story.append(Paragraph("A. Ethical Fair-Use Boundaries", h2_style))
    story.append(
        Paragraph(
            "Predictive electoral models carry democratic responsibilities: "
            "<br/>1. <b>Bandwagon Effect Mitigation:</b> Model output represents statistical historical probability, not an inevitable outcome. "
            "Publishing predictions prematurely can influence undecided voters. "
            "<br/>2. <b>Fair Treatment of Independents:</b> Independent candidates possess lower baseline probabilities due to lack of party machinery, "
            "even when individual grassroots support is strong. "
            "<br/>3. <b>Transparency & Openness:</b> All training features and validation code are open-source and auditable.",
            body,
        )
    )

    # =========================================================================
    # SECTION XI: OPERATIONAL RUNBOOK
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("XI. Operational Runbook & Execution Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    runbook_steps = [
        ("Step 1: Environment Setup", "python -m venv venv\n.\\venv\\Scripts\\activate\npip install -r requirements.txt",
         "Installs pinned dependencies: fastapi, uvicorn, scikit-learn, pandas, reportlab, pytest."),
        ("Step 2: Clean & Validate Data", "python src/cleaning.py",
         "Loads raw CSV, executes 6 cleaning stages, verifies quality gate, exports data/cleaned/elections_cleaned.csv."),
        ("Step 3: Train & Save Pipeline", "python src/train.py",
         "Enforces temporal split, trains GradientBoostingClassifier, serializes models/pipeline.joblib."),
        ("Step 4: Execute Test Suite", "pytest -v",
         "Runs all 14 unit and integration tests across data cleaning, quality gate, and API routes."),
        ("Step 5: Launch FastAPI Web App", "uvicorn src.api:app --host 0.0.0.0 --port 7860 --reload",
         "Starts ASGI server. Serves interactive frontend at http://localhost:7860 and Swagger UI at /docs."),
        ("Step 6: Docker Container Build", "docker build -t pakistan-elections-pipeline .\ndocker run -p 7860:7860 pakistan-elections-pipeline",
         "Builds python:3.12-slim image and runs isolated container exposing port 7860 for cloud deployment."),
    ]
    for step_title, step_cmd, step_desc in runbook_steps:
        story.append(Paragraph(f"<b>{step_title}</b>", h2_style))
        story.append(
            Paragraph(
                f"<font name='Courier' size='7.5' color='#0f172a'><b>{step_cmd.replace(chr(10), '<br/>')}</b></font>",
                body,
            )
        )
        story.append(Paragraph(f"<i>Expected:</i> {step_desc}", body))

    story.append(PageBreak())

    # =========================================================================
    # SECTION XII: TECHNICAL GLOSSARY (25 DEFINITIONS)
    # =========================================================================
    story.append(Paragraph("XII. Technical Glossary (Plain-English Definitions)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))

    glossary_items = [
        ("Byte Order Mark (BOM)", "An invisible Unicode byte sequence (\ufeff) placed at the start of a text file. In CSVs, it corrupts column headers unless stripped with 'utf-8-sig'."),
        ("Data Quality Gate", "An automated checkpoint that validates data against strict integrity assertions, halting the pipeline if corrupted data is detected."),
        ("Target Leakage", "A critical ML error where features that only exist after the target event occurs are accidentally included during training, causing false real-world failure."),
        ("Temporal Split", "Partitioning data strictly chronologically (training on older years, testing on newer years) to prevent future data from leaking into past predictions."),
        ("First-Past-The-Post (FPTP)", "An electoral system where the single candidate who wins the most votes in a constituency wins the entire seat, even without an absolute majority."),
        ("Class Imbalance", "A dataset condition where one target label heavily outnumbers the other. In this dataset, losing candidates outnumber winners 8-to-1 (89% vs 11%)."),
        ("PR-AUC (Precision-Recall AUC)", "The area under the Precision-Recall curve. The gold standard metric for evaluating imbalanced classification models, uninflated by large true negatives."),
        ("ROC-AUC", "The Receiver Operating Characteristic Area Under Curve. Measures a model's ability to rank winning candidates higher than losing candidates across all thresholds."),
        ("ColumnTransformer", "A scikit-learn utility that routes numeric and categorical columns through distinct preprocessing transformations while assembling a unified matrix."),
        ("One-Hot Encoding", "Converting categorical strings into binary indicator columns (0 or 1), allowing tree-based and linear models to process non-numeric variables."),
        ("StandardScaler", "Normalizing numeric features to have zero mean and unit variance, preventing high-magnitude columns from dominating distance calculations."),
        ("Gradient Boosting", "An ensemble ML algorithm that builds trees sequentially, with each new decision tree trained to predict and correct the residual errors of prior trees."),
        ("Permutation Importance", "A model inspection technique that measures the drop in model score when a feature column is randomly shuffled, quantifying each feature's contribution."),
        ("Concept Drift", "Changes in statistical relationships between features and target over time due to external shifts (e.g., party bans or delimitation redrawing)."),
        ("FastAPI", "A modern, high-performance Python web framework for building asynchronous REST APIs based on standard Python type hints."),
        ("Uvicorn", "A lightning-fast ASGI (Asynchronous Server Gateway Interface) web server implementation for Python, running frameworks like FastAPI."),
        ("Pydantic", "A data parsing and validation library that enforces Python type hints at runtime, generating friendly validation errors when inputs violate schemas."),
        ("Lifespan Event", "A FastAPI mechanism that executes initialization logic (such as loading machine learning models into memory) once at startup before handling requests."),
        ("Single-Page Application (SPA)", "A web application that interacts with the browser dynamically by rewriting the current page with new data from a server rather than reloading entire pages."),
        ("Cascading Dropdown", "A UI design pattern where selections in a parent dropdown menu automatically filter and populate the available options in dependent child dropdown menus."),
        ("StreamingResponse", "An HTTP response mechanism that transmits large datasets or generated CSVs in memory chunks directly to the client without creating temporary disk files."),
        ("Dockerfile", "A text document containing all the commands a user could call on the command line to assemble a reproducible container image."),
        ("Hugging Face Spaces", "A free cloud hosting platform that automatically builds Docker containers and serves interactive machine learning applications over public HTTPS."),
        ("Joblib", "A set of tools for lightweight pipelining and disk serialization of large Python objects and NumPy arrays, standard for saving scikit-learn pipelines."),
        ("Random Seed (random_state)", "A fixed integer value used to initialize pseudo-random number generators, guaranteeing that data splits and model training yield identical results."),
    ]
    for term, definition in glossary_items:
        story.append(Paragraph(f"• <b>{term}</b>: {definition}", body))

    story.append(PageBreak())

    # =========================================================================
    # SECTION XIII: MASTER VIVA VOCE DEFENSE Q&A (25 QUESTIONS)
    # =========================================================================
    story.append(Paragraph("XIII. Master Viva Voce & Technical Defense Q&A", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))
    story.append(
        Paragraph(
            "This section provides 25 rigorous oral defense questions and comprehensive model answers. "
            "It equips the student to defend data engineering choices, machine learning trade-offs, "
            "leakage firewall design, API architecture, and cloud deployment boundaries before examiners.",
            body,
        )
    )

    viva_questions = [
        ("Q1: What is the primary objective of this project, and why is predicting before voting day critical?",
         "The objective is to predict whether a National Assembly candidate is likely to win their seat using strictly pre-election features. "
         "Predicting before voting day is critical because post-election metrics (like actual vote tallies) do not exist when campaign decisions are made. "
         "Using pre-election features allows strategic campaign resource allocation and battleground seat identification without data leakage."),

        ("Q2: What is the Byte Order Mark (BOM) bug in the raw dataset, and how does your code resolve it?",
         "The raw CSV was exported with a UTF-8 BOM byte sequence (\\ufeff). Standard pandas <font name='Courier'>read_csv()</font> parses this as part of the first column header, "
         "producing <font name='Courier'>'\\ufeffYear'</font> instead of <font name='Courier'>'Year'</font>, which breaks schema lookups. "
         "We resolve this in <font name='Courier'>src/load_data.py</font> by explicitly specifying <font name='Courier'>encoding='utf-8-sig'</font>, which automatically strips the BOM prefix."),

        ("Q3: Why was 88.6% of the raw dataset missing voter turnout and registered voters, and how did you fix it without dropping rows?",
         "In historical ECP gazettes, seat-level metrics (Registered Voters, Turnout) were printed only on the winner's row to save paper, leaving runner-up rows blank. "
         "Dropping nulls would have destroyed 88.6% of the data. We resolved this by grouping by <font name='Courier'>['Year', 'Constituency']</font> "
         "and applying <font name='Courier'>.transform('first')</font> to forward-propagate seat-level numbers across all candidate rows in that constituency."),

        ("Q4: What is target leakage? Name three columns in the raw data that leak the target, and explain why each was dropped.",
         "Target leakage occurs when training data contains features generated after the target event occurs. "
         "Three leaking columns dropped are: 1) <font name='Courier'>Votes</font> (actual votes cast on election day), "
         "2) <font name='Courier'>Turnout N</font> (final turnout percentage calculated after polls close), and "
         "3) <font name='Courier'>vote_share_pct</font> (candidate's share of valid votes). Each gives away the winner directly."),

        ("Q5: Why did you drop the candidate's personal name from the modeling features?",
         "Candidate name is a high-cardinality textual identifier. Including it causes decision trees to memorize specific individuals "
         "rather than learning structural relationships between party strength, voter size, and candidate crowding. "
         "Dropping it ensures generalizability to new candidates."),

        ("Q6: Why did you choose a chronological train/test split (1970–2013 vs 2018–2024) instead of a random train_test_split?",
         "Random splitting causes temporal data leakage: future political outcomes would train the model to predict past elections. "
         "A chronological split simulates true real-world forecasting by training strictly on historical elections and evaluating on unseen future elections."),

        ("Q7: Your test accuracy is 89.70%. Why is accuracy misleading in this dataset, and what metric did you prioritize?",
         "In Pakistan's FPTP system, each seat has 1 winner and ~8 losers, meaning 89% of candidates lose. "
         "A naive model predicting 'loss' every time achieves 89% accuracy but has 0% recall on winners. "
         "We prioritized Precision-Recall AUC (PR-AUC: 0.5958), which measures true positive detection uninflated by large true negative counts."),

        ("Q8: What is a scikit-learn Pipeline and ColumnTransformer, and why wrap them into a single saved object?",
         "A Pipeline chains preprocessing and estimator into one object; ColumnTransformer applies different encoders to numeric vs. categorical columns. "
         "Wrapping them into a single object ensures identical preprocessing transformations during training and FastAPI serving, eliminating train-serve skew."),

        ("Q9: What algorithm is used, what are its hyperparameters, and why not use Logistic Regression?",
         "We used GradientBoostingClassifier (100 estimators, max_depth=3, learning_rate=0.1, random_state=42). "
         "Logistic regression assumes linear decision boundaries, whereas electoral contests exhibit complex non-linear interactions "
         "(e.g., party strength thresholds dependent on candidate crowding)."),

        ("Q10: What is the automated Quality Gate, and what happens if a check fails?",
         "The Quality Gate (<font name='Courier'>src/validation.py</font>) enforces 6 assertions (row count >= 20,000, zero duplicates, valid ranges, binary target). "
         "If any check fails, it raises an explicit <font name='Courier'>ValueError</font>, halting execution before corrupted data can poison model training."),

        ("Q11: Why is the data/raw/ directory treated as strictly immutable?",
         "Raw data represents the ground-truth historical record. Never editing it guarantees that data engineering steps can be audited, "
         "reproduced, or re-run from scratch whenever cleaning logic is updated."),

        ("Q12: How does FastAPI's lifespan event prevent memory exhaustion and slow request handling?",
         "Loading <font name='Courier'>pipeline.joblib</font> on every HTTP request would deserialize a 15MB file repeatedly, causing high latency and memory spikes. "
         "The lifespan context manager loads the pipeline once into RAM during server startup, enabling instant sub-10ms predictions."),

        ("Q13: What role does Pydantic play in POST /predict, and what happens when an invalid voter count is submitted?",
         "Pydantic's <font name='Courier'>CandidateInput</font> model validates incoming JSON data types and value constraints (e.g., Registered Voters > 0). "
         "If invalid data is submitted, Pydantic intercepts the request and returns an automatic HTTP 422 Unprocessable Entity error with exact field diagnostics."),

        ("Q14: Explain the cascading dropdown feature in frontend/index.html and how it prevents invalid user input.",
         "Selecting a Province (e.g., 'Sindh') dynamically filters the Region dropdown to valid divisions ('Karachi', 'Interior Sindh'), "
         "which in turn filters Electoral Zones. This prevents users from selecting physically impossible combinations (e.g., Lahore in Sindh)."),

        ("Q15: What concept drift occurred in the 2024 general election regarding PTI candidates, and how does it impact predictions?",
         "In 2024, the ECP revoked PTI's 'cricket bat' electoral symbol, forcing candidates to contest as independents under varied symbols. "
         "Because historically independent candidates rarely win, the model predicts low win probabilities unless the party is explicitly labeled as PTI."),

        ("Q16: Why does Balochistan exhibit the highest classification error rate among all Pakistani provinces?",
         "Balochistan has 44% of Pakistan's land area but only 6% of its population, resulting in low voter turnout, vast distances, "
         "and multi-cornered contests where 20+ candidates split votes, allowing winners to emerge with thin, volatile margins."),

        ("Q17: What is permutation feature importance, and what is the #1 feature in your trained model?",
         "Permutation importance measures score degradation when a feature column is randomly shuffled. "
         "Political party affiliation (<font name='Courier'>Party</font>) is the #1 feature, dropping PR-AUC by ~0.14, confirming that party machinery drives FPTP outcomes."),

        ("Q18: What is the purpose of the Six Parties feature, and why include it alongside Party?",
         "Pakistan has dozens of minor parties. <font name='Courier'>Six Parties</font> aggregates them into historical political blocs "
         "(e.g., PML factions, Religious alliances), allowing the model to generalize when encountering smaller allied parties."),

        ("Q19: How does POST /predict-batch handle a CSV file where num_candidates_in_seat is missing?",
         "The batch endpoint inspects the uploaded DataFrame. If <font name='Courier'>num_candidates_in_seat</font> is absent, "
         "it groups rows by constituency and automatically computes candidate counts before running inference."),

        ("Q20: Why return StreamingResponse for batch predictions instead of saving a file to the server disk?",
         "Streaming the CSV directly from memory avoids disk I/O bottlenecks, prevents temporary file accumulation, "
         "and allows concurrent users to download results without race conditions."),

        ("Q21: Explain the purpose of each layer in the Medallion Architecture implemented in this repository.",
         "Bronze Layer (<font name='Courier'>data/raw/</font>): Immutable raw gazettes. "
         "Silver Layer (<font name='Courier'>data/cleaned/</font>): Cleaned, typed, deduplicated tables passing quality gates. "
         "Gold Layer (<font name='Courier'>models/</font>): Serialized model artifact. "
         "Platinum Layer (<font name='Courier'>src/api.py</font>, <font name='Courier'>frontend/</font>): REST serving and UI."),

        ("Q22: Why does .gitignore explicitly contain !models/pipeline.joblib?",
         "Standard gitignore files ignore the <font name='Courier'>models/</font> folder to prevent large binary bloat. "
         "The exclamation mark (<font name='Courier'>!models/pipeline.joblib</font>) whitelists the model artifact so cloud platforms (Hugging Face, Render) can deploy without retraining."),

        ("Q23: How do you deploy this pipeline for free without keeping your local laptop powered on?",
         "We package the app into a Docker container exposing port 7860 and deploy it to Hugging Face Spaces (Docker SDK) or Render Free Web Services. "
         "Both build directly from GitHub and provide free 24/7 public HTTPS endpoints."),

        ("Q24: What is the purpose of the 14 unit and integration tests in tests/?",
         "The tests verify that every cleaning function works as intended, the quality gate catches invalid data, "
         "the API returns valid schemas, and batch CSV processing executes end-to-end without regression."),

        ("Q25: If you were given 3 more months on this project, what single architectural improvement would you implement?",
         "I would build a multi-task hierarchical Bayesian model that links candidate-level probabilities with a constituency constraint "
         "enforcing that the sum of win probabilities across all candidates in a seat strictly equals 1.0 (softmax normalization)."),
    ]

    for q_text, a_text in viva_questions:
        q_card = [
            [Paragraph(f"<b>{q_text}</b>", q_title_style)],
            [Paragraph(f"<b>Model Answer:</b> {a_text}", q_ans_style)],
        ]
        t_qc = Table(q_card, colWidths=[504])
        t_qc.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
                    ("LINELEFT", (0, 0), (0, -1), 3.0, c_secondary),
                    ("TOPPADDING", (0, 0), (-1, -1), 3.5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(KeepTogether([t_qc, Spacer(1, 4)]))

    story.append(PageBreak())

    # =========================================================================
    # SECTION XIV: OPEN QUESTIONS & HONEST RECONCILIATION
    # =========================================================================
    story.append(Paragraph("XIV. Open Questions & Honest Reconciliation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=6))
    story.append(
        Paragraph(
            "Adhering to strict IEEE ethics and project honesty rules, this section reconciles all architectural assumptions and flags "
            "open domain questions for future research:",
            body,
        )
    )

    reconcile_items = [
        ("Delimitation Crosswalk (TO CONFIRM)",
         "Pakistan revised constituency boundaries in 2018 (e.g., NA-1 Peshawar changed geographic territory between 2013 and 2018). "
         "The current pipeline treats Constituency as an identifier for candidate-count aggregation within each election year, "
         "but does not construct longitudinal constituency crosswalks across delimitations."),
        ("2024 Independent Electoral Symbol Anomaly (TO CONFIRM)",
         "In the February 2024 general election, PTI candidates were legally required to contest as independent candidates ('PTI-IND') under individual electoral symbols. "
         "The model relies heavily on historical party branding ('Party=IND' historically had a low win rate), leading to false negatives in urban 2024 seats "
         "unless the candidate party is entered as PTI or PTI-IND."),
        ("Multi-Seat Candidacy Contests (TO CONFIRM)",
         "High-profile party leaders often contest multiple National Assembly seats simultaneously in the same general election. "
         "Candidate names are excluded from modeling features to prevent memorization leakage, meaning the model evaluates seat context rather than individual politician popularity."),
    ]
    for r_title, r_body in reconcile_items:
        story.append(Paragraph(f"• <b>{r_title}</b>", h2_style))
        story.append(Paragraph(r_body, body))

    # Build the document with the NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master IEEE Handbook successfully generated at: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_handbook()
