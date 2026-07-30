#!/bin/bash

# Move into the folder containing this launcher.
cd "$(dirname "$0")" || exit 1

clear

echo "============================================================"
echo "           BRIGHTMART REPORTING AUTOMATION"
echo "============================================================"
echo
echo "Starting reporting workflow..."
echo

# Confirm that the virtual environment exists.
if [ ! -d "venv" ]; then
    echo "ERROR: BrightMart has not been set up."
    echo
    echo "The Python virtual environment is missing."
    echo
    echo "Please double-click:"
    echo
    echo "setup_brightmart.command"
    echo
    echo "After setup completes, run this report again."
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

# Activate the virtual environment.
source "venv/bin/activate"

if [ $? -ne 0 ]; then
    echo "ERROR: The BrightMart environment could not be activated."
    echo
    echo "Please run setup_brightmart.command again."
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

if ! command -v python >/dev/null 2>&1; then
    echo "ERROR: Python could not be found inside the environment."
    echo
    echo "Please run setup_brightmart.command again."
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

python -c "import pandas, openpyxl" >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "ERROR: Required Python packages are missing."
    echo
    echo "Please double-click:"
    echo
    echo "setup_brightmart.command"
    echo
    echo "This will install or repair the required packages."
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

if [ ! -d "data/raw" ]; then
    echo "The input folder does not exist."
    echo "Creating data/raw..."
    mkdir -p data/raw
fi

CSV_COUNT=$(find "data/raw" -maxdepth 1 -type f \
    -iname "*.csv" | wc -l | tr -d ' ')

if [ "$CSV_COUNT" -eq 0 ]; then
    echo "ERROR: No CSV files were found in data/raw."
    echo
    echo "Please place at least one sales CSV file inside:"
    echo
    echo "$(pwd)/data/raw"
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

echo "Input files detected: $CSV_COUNT"
echo

# Run the complete reporting pipeline.
python -m src.reporting.run_reporting_pipeline

PIPELINE_EXIT_CODE=$?

echo

if [ $PIPELINE_EXIT_CODE -eq 0 ]; then
    echo "============================================================"
    echo "REPORTING WORKFLOW COMPLETED SUCCESSFULLY"
    echo "============================================================"
    echo
    echo "Your reports and dashboard files are ready."

    open .
else
    echo "============================================================"
    echo "REPORTING WORKFLOW FAILED"
    echo "============================================================"
    echo
    echo "Please check the reports and logs folders for details."
fi

echo
read -n 1 -s -r -p "Press any key to close this window..."
echo

exit $PIPELINE_EXIT_CODE