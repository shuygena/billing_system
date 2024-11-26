FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip3 install --no-index --find-links=wheelhouse wheelhouse/*
# RUN pip3 install -r requirements.txt

WORKDIR ./bs_project

