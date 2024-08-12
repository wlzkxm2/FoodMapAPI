#!bin/sh
cd src
alembic revision --autogenerate && \
alembic upgrade head