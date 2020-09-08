FROM python:3.8-slim-buster

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY backend/pyproject.toml /app/pyproject.toml
RUN poetry install

COPY backend /app
