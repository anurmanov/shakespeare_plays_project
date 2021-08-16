FROM python:3.9.6-alpine3.14

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/lib/python3.9/site-packages

RUN apk update && \
apk --no-cache add gcc python3-dev musl-dev zlib-dev
# Для сброса кэша перед выполнением pip install $(cat requirements.txt
# example: build --build-arg CACHEBUST=$(date +%s)
ARG CACHEBUST=1

COPY ./app/app.py .
COPY ./app/requirements.txt .

RUN pip install --upgrade pip && \
pip install --ignore-installed $(cat requirements.txt)
