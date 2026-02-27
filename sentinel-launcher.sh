#!/bin/bash
# Hardcoded path to your project folder
PROJECT_DIR="/Users/rohands/Desktop/Sentinel-Sentry"

# Activate the virtual environment from the project folder
source "$PROJECT_DIR/venv/bin/activate"

# Run the script using the project folder path
python3 "$PROJECT_DIR/main.py" "$@"
