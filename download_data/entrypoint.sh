#!/bin/sh

echo "Starting entrypoint.sh"

echo "Downloading kaggle data"
python -u download_kaggle.py
echo "Data downloaded"

echo "Downloading data"
python -u download_data.py
echo "Data downloaded"