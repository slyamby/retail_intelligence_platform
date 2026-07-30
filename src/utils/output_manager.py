import shutil
from pathlib import Path

from src.utils.logger import logger


def remove_existing_outputs(output_files: list[Path]) -> None:
    """
    Remove known generated outputs before a new run
    """

    for file_path in output_files:
        if file_path.exists():
            file_path.unlink()

            logger.info(
                "Removed stale output: %s",
                file_path,
            )


def prepare_staging_directory(
    staging_dir: Path,
) -> None:
    """
    Create an empty staging directory.
    """

    if staging_dir.exists():
        shutil.rmtree(staging_dir)

    staging_dir.mkdir(parents=True, exist_ok=True)


def publish_staged_outputs(
    staged_files: list[Path],
    final_directory: Path,
) -> list[Path]:
    """
    Move successfully generated files from staging
    into the final output directory.
    """

    final_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    published_files: list[Path] = []

    for staged_file in staged_files:
        final_path = final_directory / staged_file.name

        staged_file.replace(final_path)

        published_files.append(final_path)

        logger.info(
            "Published output: %s",
            final_path,
        )

    return published_files


def verify_expected_outputs(
    generated_files: list[Path], expected_filenames: set[str]
) -> None:
    """
    Confirm that all expected output files were created.
    """

    generated_names = {
        file_path.name for file_path in generated_files if file_path.exists()
    }

    missing_files = expected_filenames - generated_names

    if missing_files:
        raise RuntimeError(
            "The pipeline did not generate all "
            f"required outputs. Missing: "
            f"{sorted(missing_files)}"
        )

    empty_files = [
        file_path.name
        for file_path in generated_files
        if (file_path.exists() and file_path.stat().st_size == 0)
    ]

    if empty_files:
        raise RuntimeError(
            "The following output files are empty: " f"{sorted(empty_files)}"
        )
