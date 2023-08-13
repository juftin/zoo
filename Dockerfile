FROM python:3.11

WORKDIR /home/zoo

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-deps

COPY zoo/ zoo/
COPY README.md README.md
COPY pyproject.toml pyproject.toml
