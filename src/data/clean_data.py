from pathlib import Path

import pandas as pd

from src.utils.logger import logger

from validate import validate_sales_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

BRANCH_MAPPING = {
    "accra central": "Accra Central",
    "east legon": "East Legon",
    "kumasi": "Kumasi",
    "takoradi": "Takoradi",
    "tema": "Tema",
}

PRODUCT_MAPPING = {
    "printer": "Printer",
    "office printer": "Printer",
    "laptop": "Laptop",
    "laptops": "Laptop",
    "keyboard": "Keyboard",
    "key board": "Keyboard",
    "monitor": "Monitor",
    "led monitor": "Monitor",
    "mouse": "Mouse",
    "wireless mouse": "Mouse",
}

PAYMENT_METHOD_MAPPING = {
    "card": "Card",
    "mobile money": "Mobile Money",
    "momo": "Mobile Money",
    "cash": "Cash",
    "bank transfer": "Bank Transfer",
}


def load_data() -> pd.DataFrame:

    """
    Load every CSV file from the raw folder.

    Returns
    -------
    pandas.DataFrame
    """
    csv_files = list(
        RAW_DATA_DIR.glob("*.csv")
    )

    dataframes = []

    for file in csv_files:
        df = pd.read_csv(file)

        df["source_file"] = file.name

        dataframes.append(df)

    return pd.concat(
        dataframes,
        ignore_index=True
    )


def remove_duplicate_rows(
        data: pd.DataFrame
) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """

    before = len(data)

    data = data.drop_duplicates()

    after = len(data)

    logger.info(
        f"Removed {before-after} duplicates."
    )

    return data


def clean_branch_names(
        data: pd.DataFrame
) -> pd.DataFrame:
    """
    Standardize branch names.
    """
    data["branch"] = (
        data["branch"]
        .str.strip()
        .str.title()
    )

    return data


def clean_product_names(
        data: pd.DataFrame
) -> pd.DataFrame:
    data["product"] = (
        data["product"]
        .str.strip()
        .str.title()
    )

    return data


def clean_branch_names(data: pd.DataFrame) -> pd.DataFrame:
    """Standardise branch names using approved business mappings."""

    data = data.copy()

    normalised_branch = (
        data["branch"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    mapped_branch = normalised_branch.map(BRANCH_MAPPING)

    unmapped_values = (
        normalised_branch[mapped_branch.isna()]
        .dropna()
        .unique()
    )

    if len(unmapped_values) > 0:
        print(
            "Warning: Unmapped product values found:",
            unmapped_values.tolist(),
        )

    data["branch"] = mapped_branch

    return data


def clean_product_names(data: pd.DataFrame) -> pd.DataFrame:
    """Standardize product names using approved business mappings"""

    data = data.copy()

    normalised_products = (
        data["product"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    mapped_product = normalised_products.map(PRODUCT_MAPPING)

    unmapped_values = (
        normalised_products[mapped_product.isna()]
        .dropna()
        .unique()
    )

    if len(unmapped_values) > 0:
        print(
            "Warning: Unmapped product values found:",
            unmapped_values.tolist(),
        )

    data["product"] = mapped_product

    return data


def clean_payment_methods(data: pd.DataFrame) -> pd.DataFrame:
    """Standardize payment method names using approved business mappings"""

    data = data.copy()

    normalised_payment_method = (
        data["payment_method"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    mapped_payment_method = normalised_payment_method.map(PAYMENT_METHOD_MAPPING)

    unmapped_values = (
        normalised_payment_method[mapped_payment_method.isna()]
        .dropna()
        .unique()
    )

    if len(unmapped_values) > 0:
        print(
            "Warning: Unmapped payment method found:",
            unmapped_values.tolist(),
        )

    data["payment_method"] = mapped_payment_method

    return data


def clean_dates(data: pd.DataFrame) -> pd.DataFrame:
    """ Convert transaction_date to datetime"""

    data = data.copy()

    data["transaction_date"] = pd.to_datetime(
        data["transaction_date"],
        errors="coerce",
        dayfirst=True
    )

    return data


def clean_unit_prices(data: pd.DataFrame) -> pd.DataFrame:
    """
    Convert unit prices to numeric values
    """

    data = data.copy()

    data["unit_price"] = (
        data["unit_price"]
        .astype("string")
        .str.replace("GHS", "", regex=False)
        .str.replace("₵", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    data["unit_price"] = pd.to_numeric(
        data["unit_price"],
        errors="coerce"
    )

    return data


def clean_quantities(data: pd.DataFrame) -> pd.DataFrame:
    """
    Validate quantities
    """

    data = data.copy()

    data["quantity"] = pd.to_numeric(
        data["quantity"],
        errors="coerce"
    )

    invalid_quantity = data["quantity"] <= 0

    logger.warning(
        f"Invalid quantities: {invalid_quantity.sum()}"
    )

    return data


def handle_missing_values(
        data: pd.DataFrame
) -> pd.DataFrame:
    
    data = data.copy()

    data["customer"] = (
        data["customer"]
        .fillna("Unknown")
    )

    return data


def main():

    data = load_data()

    data = clean_branch_names(data)

    data = clean_product_names(data)

    data = clean_payment_methods(data)

    data = clean_dates(data)

    data = clean_unit_prices(data)

    data = clean_quantities(data)

    data = handle_missing_values(data)

    data = remove_duplicate_rows(data)

    issues = validate_sales_data(data)

    print(data.head())
    
    print(issues)


if __name__ == "__main__":
    main()


