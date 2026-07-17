from pathlib import Path

# ======================================================
# Project Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = PROJECT_ROOT / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

REPORT_DIR = PROJECT_ROOT / "reports"

LOG_DIR = PROJECT_ROOT / "logs"

EXCEL_DIR = PROJECT_ROOT / "excel"

# ======================================================
# Files
# ======================================================

MASTER_DATASET = PROCESSED_DATA_DIR / "master_sales.csv"

PIPELINE_LOG = LOG_DIR / "pipeline.log"