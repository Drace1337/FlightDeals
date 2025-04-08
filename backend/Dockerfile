FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && apt-get clean

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

CMD flask run --host=0.0.0.0