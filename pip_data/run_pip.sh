#!/bin/bash

echo "Starting Pip..."

# Activate virtual environment if used (uncomment if needed)
# source venv/bin/activate

# Start UART listener (runs in background)
python3 sbc_uart_receiver.py &

# Start Pip's AI core
python3 pip_ai.py
