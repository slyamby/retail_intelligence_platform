from datetime import datetime
from pathlib import Path
from typing import Iterable

from config.settings import PIPELINE_SUMMARY_REPORT
from src.utils.logger import logger
from src.utils.pipeline_stats import PipelineStatistics


def create_timestamped_report_path(
    base_path: Path = PIPELINE_SUMMARY_REPORT,
) -> Path:
    """
    Create a timestamped report path.

    Example:
        pipeline_summary_20260723_101530.txt
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{base_path.stem}_{timestamp}" f"{base_path.suffix}"

    return base_path.with_name(filename)


def build_summary_report(
    pipeline_stats: PipelineStatistics,
    dashboard_files_generated: int,
    total_execution_time: float,
    execution_status: str,
    generated_files: Iterable[Path],
    business_insights: Iterable[str] | None = None,
    error_message: str | None = None,
):
    """
    Build the BrightMart pipeline summary report.

    Parameters
    ----------
    pipeline_stats:
        Statistics returned by the cleaning pipeline.

    dashboard_files_generated:
        Number of dashboard datasets created.

    total_execution_time:
        Total reporting workflow duration in seconds.

    execution_status:
        Overall reporting workflow status.

    generated_files:
        Collection of output file paths.

    error_message:
        Optional failure message.

    Returns
    -------
    str
        Formatted report content.
    """

    generated_file_lines = "\n".join(f"- {file_path}" for file_path in generated_files)

    if not generated_file_lines:
        generated_file_lines = "- None"

    insight_lines = "\n".join(f"- {insight}" for insight in (business_insights or []))

    if not insight_lines:
        insight_lines = "- No business insights generated."

    report_lines = [
        "=" * 70,
        "BRIGHTMART REPORTING PIPELINE SUMMARY",
        "=" * 70,
        "",
        f"Execution date: " f"{datetime.now():%d %B %Y}",
        f"Execution time: " f"{datetime.now():%H:%M:%S}",
        f"Overall status: {execution_status}",
        "",
        "DATA CLEANING SUMMARY",
        "-" * 70,
        f"Rows loaded: " f"{pipeline_stats.rows_loaded}",
        f"Rows after cleaning: " f"{pipeline_stats.rows_after_cleaning}",
        f"Duplicates removed: " f"{pipeline_stats.duplicates_removed}",
        f"Customer names filled: " f"{pipeline_stats.customer_names_filled}",
        f"Invalid quantities detected: " f"{pipeline_stats.invalid_quantities}",
        f"Invalid dates detected: " f"{pipeline_stats.invalid_dates}",
        f"Cleaning pipeline status: " f"{pipeline_stats.execution_status}",
        f"Cleaning pipeline duration: " f"{pipeline_stats.execution_time:.2f} seconds",
        "",
        "DASHBOARD SUMMARY",
        "-" * 70,
        f"Dashboard files generated: " f"{dashboard_files_generated}",
        "",
        "BUSINESS INSIGHTS",
        "-" * 70,
        insight_lines,
        "",
        "GENERATED OUTPUT FILES",
        "-" * 70,
        generated_file_lines,
        "",
        "EXECUTION SUMMARY",
        "-" * 70,
        f"Total execution time: " f"{total_execution_time:.2f} seconds",
        f"Final status: {execution_status}",
    ]

    if error_message:
        report_lines.extend(
            [
                "",
                "ERROR DETAILS",
                "-" * 70,
                error_message,
            ]
        )

    report_lines.extend(["", "=" * 70])

    return "\n".join(report_lines)


def save_summary_report(
    report_content: str,
    output_path: Path | None = None,
) -> Path:
    """
    Save the pipeline summary report to disk.

    Returns
    -------
    Path
        Location of the saved report.
    """

    if output_path is None:
        output_path = create_timestamped_report_path()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(report_content, encoding="utf-8")

    logger.info("Pipeline summary report saved to %s", output_path)

    return output_path
