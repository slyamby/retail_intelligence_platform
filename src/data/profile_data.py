from pathlib import Path

import pandas as pd


# -------------------------------------
# Paths
# -------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"



# ------------------------------------
# Read Every CSV file
# ------------------------------------

csv_files = list(RAW_DATA_DIR.glob("*.csv"))

dataframes = []

for file in csv_files:

    df = pd.read_csv(file)

    df["source_file"] = file.name

    dataframes.append(df)

sales_data = pd.concat(
    dataframes,
    ignore_index=True
)

print("=" * 70)
print("FIRST FIVE ROWS")
print("=" * 70)

print(sales_data.head())

print()

print("=" * 70)
print("COLUMN INFORMATION")
print("=" * 70)

print(sales_data.info())

print()
print("=" * 70)
print("MISSING VALUES")
print("=" * 70)

print(sales_data.isnull().sum())

print()
print("=" * 70)
print("DUPLICATE ROWS")
print("=" * 70)

print(sales_data.duplicated().sum())

print()
print("=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)

print(sales_data.describe(include="all"))

categorical_columns = [
    "branch",
    "product",
    "payment_method"
]

for column in categorical_columns:

    print()
    
    print("=" * 70)
    print(column.upper())
    print("=" * 70)

    print(sales_data[column].value_counts(dropna=False))