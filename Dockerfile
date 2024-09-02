FROM python:3.8-slim-buster

MORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install requirements.txt

COPY

CHD gunicorn app:app & python main.py
