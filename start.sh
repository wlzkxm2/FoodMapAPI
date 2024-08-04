#!bin/bash
cd src
uvicorn main:app --reload --port 8111 --host localhost