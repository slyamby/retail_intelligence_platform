import random
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

# This file is located in:
# retail-intelligence-platform/src/data/generate_raw_data.py
#
# parents[0] = src/data
# parents[1] = src
# parents[2] = project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Create the folder if it does not already exist.
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


BRANCHES = {
    "Accra Central": [
        "Accra Central",
        "accra central",
        "ACCRA CENTRAL",
        " Accra Central ",
    ],
    "East Legon": ["East Legon", "east legon", "EAST LEGON", " East Legon"],
    "Kumasi": ["Kumasi", "kumasi", "KUMASI", " Kumasi "],
    "Takoradi": ["Takoradi", "takoradi", "TAKORADI", "Takoradi "],
    "Tema": ["Tema", "tema", "TEMA", " Tema"],
}


PRODUCTS = {
    "Laptop": ["Laptop", "laptop", "LAPTOP", " Laptop ", "Laptops"],
    "Mouse": ["Mouse", "mouse", "MOUSE", "Wireless Mouse", " Mouse "],
    "Keyboard": ["Keyboard", "keyboard", "KEYBOARD", "Key board", " Keyboard "],
    "Monitor": ["Monitor", "monitor", "MONITOR", "LED Monitor", " Monitor "],
    "Printer": ["Printer", "printer", "PRINTER", "Office Printer", " Printer "],
}


UNIT_PRICES = {
    "Laptop": 6500.00,
    "Mouse": 150.00,
    "Keyboard": 350.00,
    "Monitor": 1800.00,
    "Printer": 2500.00,
}


DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%b-%Y",
]


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------


def create_transaction_id(branch_code: str, transaction_number: int) -> str:
    """Create a unique transaction ID."""

    return f"{branch_code}-{transaction_number:05d}"


def format_date(date_value: pd.Timestamp) -> str:
    """Return the date in one of several inconsistent formats."""

    selected_format = random.choice(DATE_FORMATS)
    return date_value.strftime(selected_format)


def format_price(price: float) -> str | float:
    """
    Randomly return a clean numeric price or a messy string price.

    Examples:
    6500
    GHS 6,500.00
    ₵6500.00
    " 6500.0 "
    """

    options = [
        price,
        f"GHS {price:,.2f}",
        f"₵{price:,.2f}",
        f" {price:.2f} ",
    ]

    return random.choice(options)


def introduce_missing_value(value, probability: float = 0.03):
    """Replace a value with a missing value based on a probability."""

    if random.random() < probability:
        return np.nan

    return value


def generate_branch_data(
    branch_name: str,
    branch_code: str,
    start_transaction_number: int,
    number_of_rows: int = 80,
) -> pd.DataFrame:
    """Generate intentionally messy retail sales data for one branch."""

    records = []

    start_date = pd.Timestamp("2026-01-01")
    end_date = pd.Timestamp("2026-03-31")

    available_dates = pd.date_range(start_date, end_date, freq="D")

    for row_number in range(number_of_rows):
        canonical_product = random.choice(list(PRODUCTS.keys()))
        quantity = random.randint(1, 8)
        unit_price = UNIT_PRICES[canonical_product]

        transaction_date = random.choice(available_dates)

        # Occasionally create unrealistic or invalid quantities.
        if random.random() < 0.04:
            quantity = random.choice([0, -1, -3, 100])

        transaction_id = create_transaction_id(
            branch_code=branch_code,
            transaction_number=start_transaction_number + row_number,
        )

        branch_variation = random.choice(BRANCHES[branch_name])
        product_variation = random.choice(PRODUCTS[canonical_product])

        record = {
            "transaction_id": transaction_id,
            "transaction_date": format_date(transaction_date),
            "branch": branch_variation,
            "product": product_variation,
            "quantity": introduce_missing_value(quantity, probability=0.03),
            "unit_price": introduce_missing_value(
                format_price(unit_price),
                probability=0.03,
            ),
            "customer_name": introduce_missing_value(
                random.choice(
                    [
                        "Ama Mensah",
                        "Kwame Asante",
                        "Yaw Boateng",
                        "Akosua Owusu",
                        "Kofi Addo",
                        "Esi Arthur",
                    ]
                ),
                probability=0.08,
            ),
            "payment_method": random.choice(
                [
                    "Cash",
                    "cash",
                    "CASH",
                    "Mobile Money",
                    "Momo",
                    "Card",
                    "card",
                    "Bank Transfer",
                ]
            ),
        }

        records.append(record)

    dataframe = pd.DataFrame(records)

    # Add duplicate rows intentionally.
    duplicate_count = max(2, int(number_of_rows * 0.05))

    duplicates = dataframe.sample(
        n=duplicate_count,
        random_state=RANDOM_SEED,
    )

    dataframe = pd.concat(
        [dataframe, duplicates],
        ignore_index=True,
    )

    # Shuffle the rows so duplicates are not grouped together.
    dataframe = dataframe.sample(
        frac=1,
        random_state=RANDOM_SEED,
    ).reset_index(drop=True)

    return dataframe


# ---------------------------------------------------------
# Main programme
# ---------------------------------------------------------


def main() -> None:
    """Generate raw CSV files for all BrightMart branches."""

    branch_codes = {
        "Accra Central": "ACC",
        "East Legon": "EAS",
        "Kumasi": "KUM",
        "Takoradi": "TAK",
        "Tema": "TEM",
    }

    starting_numbers = {
        "Accra Central": 10001,
        "East Legon": 20001,
        "Kumasi": 30001,
        "Takoradi": 40001,
        "Tema": 50001,
    }

    for branch_name, branch_code in branch_codes.items():
        branch_data = generate_branch_data(
            branch_name=branch_name,
            branch_code=branch_code,
            start_transaction_number=starting_numbers[branch_name],
            number_of_rows=80,
        )

        output_filename = branch_name.lower().replace(" ", "_").strip() + "_sales.csv"

        output_path = RAW_DATA_DIR / output_filename

        branch_data.to_csv(
            output_path,
            index=False,
        )

        print(f"Created {output_filename}: " f"{len(branch_data)} rows")

    print(f"\nRaw data saved to: {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()
