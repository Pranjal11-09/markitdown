#!/bin/bash
# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install requirements
echo "Installing dependencies..."
.venv/bin/pip install -r requirements.txt

# Run the streamlit application
echo "Starting Streamlit application..."
.venv/bin/streamlit run app.py
