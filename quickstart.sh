#!/bin/bash

echo "========================================"
echo "Jeevan-Amrit Backend Quick Start"
echo "========================================"
echo ""

echo "[1/4] Activating virtual environment..."
source venv/bin/activate

echo "[2/4] Installing dependencies..."
pip install -r requirements.txt

echo "[3/4] Checking MongoDB..."
if ! pgrep -x "mongod" > /dev/null
then
    echo "Starting MongoDB..."
    brew services start mongodb-community 2>/dev/null || sudo systemctl start mongod 2>/dev/null
fi

echo "[4/4] Starting Flask backend..."
python app.py
