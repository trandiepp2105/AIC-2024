#!/bin/sh

echo "Starting entrypoint.sh"

echo "Downloading data"
cd download_data
# python -u download_data.py
echo "Data downloaded"

echo "Running setup.py"
cd ..
python -u setup.py
echo "setup.py complete"