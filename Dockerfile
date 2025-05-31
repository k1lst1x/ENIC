FROM python:3.11.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gcc

WORKDIR /usr/src/app

COPY req.txt /usr/src/app/req.txt

RUN pip install --upgrade pip && \
    pip install -r req.txt

COPY . /usr/src/app/