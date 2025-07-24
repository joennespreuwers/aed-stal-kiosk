#!/bin/bash
set -e

# Go to script directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
    deactivate
    exit 1
fi

deactivate

# Make run_backend.sh executable if it exists
if [ -f run_backend.sh ]; then
    chmod +x run_backend.sh
fi

echo "Installation complete."
