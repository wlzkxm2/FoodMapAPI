#!bin/bash
cd src
uvicorn main:app --reload --port 8112 --host localhost