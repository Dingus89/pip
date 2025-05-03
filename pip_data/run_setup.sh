#!/bin/bash

cd "$(pip_data "$0")"
echo "Running initial Pip setup..."

echo "[1/3] Creating folders..."
mkdir -p pip_data
mkdir -p models
mkdir -p tmp_audio

echo "[2/3] Checking config..."
python3 verify_pip_config.py

echo "[3/3] Installing Python dependencies..."
pip3 install -r requirements.txt

echo "✅ Pip setup complete. You can now run ./run_pip.sh"