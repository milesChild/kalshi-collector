#!/bin/bash

# Python script location
PY_SCRIPT="/opt/kalshi/kalshi-collector/src/redis_app.py"

# File to save the PIDs of spawned processes
PIDS_FILE="pids.log"

# Clear the PIDs file
> "$PIDS_FILE"

python "$PY_SCRIPT" &
echo $! >> "$PIDS_FILE"