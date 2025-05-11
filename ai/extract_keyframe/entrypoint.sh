#!/bin/bash

echo "Starting download_onedrive.py"
python download_onedrive.py
echo "Download completed"

echo "Starting extract_keyframes.py"
python embedding_keyframes.py
echo "Extraction completed"