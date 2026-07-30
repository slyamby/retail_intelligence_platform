import pandas as pd

from src.validation.input_validator import validate_csv_file


def test_validate_csv_file_accepts_valid_file(
    sample_sales_data,
    tmp_path,
):
    """
    A valid sales CSV should return no errors.
    """

    input_file = tmp_path / "sales.csv"

    sample_sales_data.to_csv(
        input_file,
        index=False,
    )

    errors = validate_csv_file(input_file)

    assert errors == []


def test_validate_csv_file_rejects_empty_file(
    tmp_path,
):
    """
    An empty CSV should be rejected.
    """

    input_file = tmp_path / "empty.csv"

    input_file.touch()

    errors = validate_csv_file(input_file)

    assert len(errors) == 1
    assert "empty" in errors[0].lower()


def test_validate_csv_file_rejects_missing_columns(
    sample_sales_data,
    tmp_path,
):
    """
    A CSV missing a required column should
    return a validation error.
    """

    incomplete_data = sample_sales_data.drop(columns=["quantity"])

    input_file = tmp_path / "incomplete.csv"

    incomplete_data.to_csv(
        input_file,
        index=False,
    )

    errors = validate_csv_file(input_file)

    assert len(errors) > 0

    assert any("quantity" in error.lower() for error in errors)
