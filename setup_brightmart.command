#!/bin/bash

# Move into the project directory.
cd "$(dirname "$0")" || exit 1

clear

echo "============================================================"
echo "             BRIGHTMART INITIAL SETUP"
echo "============================================================"
echo
echo "This setup will:"
echo "- Check for Python"
echo "- Create a virtual environment"
echo "- Install required packages"
echo "- Create required project folders"
echo
echo "Setup is normally required only once."
echo

# ------------------------------------------------------------
# Check whether Python 3 is installed.
# ------------------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 was not found."
    echo
    echo "Please install Python 3 before continuing."
    echo "You can obtain it from the official Python website."
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

PYTHON_VERSION=$(python3 --version)

echo "Python detected: $PYTHON_VERSION"
echo

# ------------------------------------------------------------
# Check whether requirements.txt exists.
# ------------------------------------------------------------

if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt was not found."
    echo
    echo "Expected location:"
    echo "$(pwd)/requirements.txt"
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

# ------------------------------------------------------------
# Create the virtual environment if it does not exist.
# ------------------------------------------------------------

if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    echo "Creating virtual environment..."

    python3 -m venv venv

    if [ $? -ne 0 ]; then
        echo
        echo "ERROR: Virtual environment creation failed."
        echo
        read -n 1 -s -r -p "Press any key to close..."
        echo
        exit 1
    fi

    echo "Virtual environment created successfully."
fi

echo

# ------------------------------------------------------------
# Activate the virtual environment.
# ------------------------------------------------------------

source "venv/bin/activate"

if [ $? -ne 0 ]; then
    echo "ERROR: Could not activate the virtual environment."
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

echo "Virtual environment activated."
echo

# ------------------------------------------------------------
# Upgrade pip.
# ------------------------------------------------------------

echo "Updating package installer..."

python -m pip install --upgrade pip

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: pip could not be updated."
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

echo

# ------------------------------------------------------------
# Install dependencies.
# ------------------------------------------------------------

echo "Installing project dependencies..."

python -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Dependency installation failed."
    echo
    echo "Check your internet connection and try again."
    echo
    read -n 1 -s -r -p "Press any key to close..."
    echo
    exit 1
fi

echo
echo "Dependencies installed successfully."
echo

# ------------------------------------------------------------
# Create required folders.
# ------------------------------------------------------------

echo "Creating required project folders..."

mkdir -p data/raw
mkdir -p data/processed
mkdir -p reports
mkdir -p logs

echo "Required folders are ready."
echo

# ------------------------------------------------------------
# Confirm important project files.
# ------------------------------------------------------------

if [ ! -f "src/reporting/run_reporting_pipeline.py" ]; then
    echo
    echo "WARNING: The reporting pipeline file was not found."
    echo
    echo "Expected:"
    echo "src/reporting/run_reporting_pipeline.py"
    echo
fi

echo
echo "============================================================"
echo "SETUP COMPLETED SUCCESSFULLY"
echo "============================================================"
echo
echo "Next steps:"
echo
echo "1. Place sales CSV files inside data/raw"
echo "2. Double-click run_brightmart_report.command"
echo
echo "The BrightMart reporting platform is ready."
echo
read -n 1 -s -r -p "Press any key to close this window..."
echo