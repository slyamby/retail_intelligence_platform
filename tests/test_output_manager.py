import pytest

from src.utils.output_manager import verify_expected_outputs


def test_verify_expected_outputs_passes(
    tmp_path,
):
    """
    Verification should pass when all expected
    non-empty files exist.
    """

    expected_names = {
        "master_sales.csv",
        "dashboard_kpis.csv",
    }

    master_file = tmp_path / "master_sales.csv"

    kpi_file = tmp_path / "dashboard_kpis.csv"

    master_file.write_text(
        "column\nvalue\n",
        encoding="utf-8",
    )

    kpi_file.write_text(
        "metric\nvalue\n",
        encoding="utf-8",
    )

    generated_files = [
        master_file,
        kpi_file,
    ]

    verify_expected_outputs(
        generated_files=generated_files,
        expected_filenames=expected_names,
    )


def test_verify_expected_outputs_rejects_missing_file(
    tmp_path,
):
    """
    Verification should fail when an expected
    output file is missing.
    """

    master_file = tmp_path / "master_sales.csv"

    master_file.write_text(
        "column\nvalue\n",
        encoding="utf-8",
    )

    with pytest.raises(
        RuntimeError,
        match="Missing",
    ):
        verify_expected_outputs(
            generated_files=[master_file],
            expected_filenames={
                "master_sales.csv",
                "dashboard_kpis.csv",
            },
        )
