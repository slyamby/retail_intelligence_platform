from pathlib import Path

import pandas as pd

from config.settings import REQUIRED_SALES_COLUMNS
from src.utils.logger import logger


def normalise_column_name(
    column_name: str,
) -> str:
    """
    Convert a column name to lowercase snake case.
    """

    return str(column_name).strip().lower().replace(" ", "_")


def validate_csv_file(
    file_path: Path,
) -> list[str]:
    """
    Validate one raw CSV file.

    Returns a list of validation errors.
    An empty list means the file passed validation.
    """

    errors: list[str] = []

    if not file_path.exists():
        return [f"File does not exist: {file_path}"]

    if file_path.suffix.lower() != ".csv":
        return [f"Unsupported file type: {file_path.name}"]

    if file_path.stat().st_size == 0:
        return [f"File is empty: {file_path.name}"]

    try:
        sample = pd.read_csv(
            file_path,
            nrows=10,
        )

    except pd.errors.EmptyDataError:
        return [f"File contains no readable data: " f"{file_path.name}"]

    except pd.errors.ParserError as error:
        return [f"CSV parsing failed for " f"{file_path.name}: {error}"]

    except UnicodeDecodeError as error:
        return [f"Text encoding could not be read for " f"{file_path.name}: {error}"]

    except OSError as error:
        return [f"File could not be opened: " f"{file_path.name}: {error}"]

    sample.columns = [normalise_column_name(column) for column in sample.columns]

    missing_columns = REQUIRED_SALES_COLUMNS - set(sample.columns)

    if missing_columns:
        errors.append(
            f"{file_path.name} is missing required "
            f"columns: {sorted(missing_columns)}"
        )

    if len(sample.columns) != len(set(sample.columns)):
        errors.append(
            f"{file_path.name} contains duplicate " "column names after normalisation."
        )

    return errors


def get_raw_csv_files(
    raw_data_dir: Path,
) -> list[Path]:
    """
    Return all CSV files in the raw-data folder.
    """

    return sorted(
        file_path
        for file_path in raw_data_dir.iterdir()
        if (file_path.is_file() and file_path.suffix.lower() == ".csv")
    )


def validate_schema_consistency(
    file_paths: list[Path],
) -> None:
    """
    Confirm that all input files use the same
    normalised column structure.
    """

    reference_columns: set[str] | None = None
    reference_file: str | None = None
    differences: list[str] = []

    for file_path in file_paths:
        header = pd.read_csv(
            file_path,
            nrows=0,
        )

        columns = {normalise_column_name(column) for column in header.columns}

        if reference_columns is None:
            reference_columns = columns
            reference_file = file_path.name
            continue

        if columns != reference_columns:
            missing = reference_columns - columns

            additional = columns - reference_columns

            differences.append(
                f"{file_path.name} differs from "
                f"{reference_file}. "
                f"Missing: {sorted(missing)}. "
                f"Additional: {sorted(additional)}."
            )

    if differences:
        details = "\n".join(f"- {difference}" for difference in differences)

        raise ValueError("Input file schemas are inconsistent: \n" f"{details}")


def validate_raw_input_files(
    raw_data_dir: Path,
) -> list[Path]:
    """
    Validate all raw CSV files.

    Returns
    -------
    list[Path]
        Files approved for processing.

    Raises
    ------
    FileNotFoundError
        If the raw-data folder does not exist.

    ValueError
        If there are no CSV files or any file
        fails validation.
    """

    if not raw_data_dir.exists():
        raise FileNotFoundError(f"Raw-data folder not found: " f"{raw_data_dir}")

    csv_files = get_raw_csv_files(raw_data_dir)

    if not csv_files:
        raise ValueError(f"No CSV files were found in " f"{raw_data_dir}.")

    all_errors: list[str] = []

    for file_path in csv_files:
        file_errors = validate_csv_file(file_path)

        all_errors.extend(file_errors)

    if all_errors:
        formated_errors = "\n".join(f"- {error}" for error in all_errors)

        raise ValueError("Input validation failed: \n" f"{formated_errors}")

    validate_schema_consistency(csv_files)

    logger.info(
        "%s input CSV files passed validation.",
        len(csv_files),
    )

    return csv_files
