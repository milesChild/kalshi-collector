#!/bin/bash

# Location of the tickers.txt file
TICKERS_FILE="/opt/kalshi/tickers.txt"

# Python script location
PY_SCRIPT="/opt/kalshi/kalshi-collector/src/app.py"

# File to save the PIDs of spawned processes
PIDS_FILE="pids.log"

# Check if tickers.txt file exists
if [[ ! -f "$TICKERS_FILE" ]]; then
    echo "Error: $TICKERS_FILE not found."
    exit 1
fi

# Clear the PIDs file
> "$PIDS_FILE"

# Loop through each ticker in tickers.txt
while IFS= read -r ticker; do
    # Spawn a new python process for each ticker
    python "$PY_SCRIPT" "$ticker" &

    # Log the PID
    echo $! >> "$PIDS_FILE"
done < "$TICKERS_FILE"

echo "All processes started. Check $PIDS_FILE for the list of PIDs."
