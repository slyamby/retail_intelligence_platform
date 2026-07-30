from pathlib import Path

# ======================================================
# Project Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

REPORT_DIR = PROJECT_ROOT / "reports"

LOG_DIR = PROJECT_ROOT / "logs"

EXCEL_DIR = PROJECT_ROOT / "excel"

PIPELINE_SUMMARY_REPORT = REPORT_DIR / "pipeline_summary.txt"

BUSINESS_INSIGHTS_REPORT = REPORT_DIR / "business_insights.txt"

STAGING_DATA_DIR = DATA_DIR / "staging"

# ======================================================
# Files
# ======================================================

MASTER_DATASET = PROCESSED_DATA_DIR / "master_sales.csv"

PIPELINE_LOG = LOG_DIR / "pipeline.log"

# =====================================================
# Columns
# =====================================================

REQUIRED_SALES_COLUMNS = {
    "transaction_date",
    "branch",
    "product",
    "quantity",
    "unit_price",
    "customer_name",
    "payment_method",
}

# ===================================================
# Output Paths
# ===================================================

DASHBOARD_KPI_FILE = PROCESSED_DATA_DIR / "dashboard_kpis.csv"

REVENUE_BY_BRANCH_FILE = PROCESSED_DATA_DIR / "revenue_by_branch.csv"

REVENUE_BY_PRODUCT_FILE = PROCESSED_DATA_DIR / "revenue_by_product.csv"

MONTHLY_REVENUE_FILE = PROCESSED_DATA_DIR / "revenue_by_month.csv"

PAYMENT_METHOD_FILE = PROCESSED_DATA_DIR / "payment_method_by_revenue.csv"

TOP_CUSTOMERS_FILE = PROCESSED_DATA_DIR / "top_10_customers_by_revenue.csv"

REPORTING_OUTPUT_FILES = [
    MASTER_DATASET,
    DASHBOARD_KPI_FILE,
    REVENUE_BY_BRANCH_FILE,
    REVENUE_BY_PRODUCT_FILE,
    MONTHLY_REVENUE_FILE,
    PAYMENT_METHOD_FILE,
    TOP_CUSTOMERS_FILE,
]

EXPECTED_OUTPUT_FILENAMES = {
    "master_sales.csv",
    "dashboard_kpis.csv",
    "revenue_by_branch.csv",
    "revenue_by_product.csv",
    "monthly_revenue.csv",
    "payment_methods.csv",
    "top_customers.csv",
}
