#!/bin/sh


echo "Starting cloud server"

# Chạy FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 --reload