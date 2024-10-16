# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION
ARG ALPINE_VERSION

FROM python:3.12-alpine

ARG BGBOT_GITHUB_URL
RUN apk add --no-cache git \
    && git clone https://github.com/smartpetrol/ct-company-python-bot/tree/sigora/2371_adaptation.git

WORKDIR /BGBot
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]