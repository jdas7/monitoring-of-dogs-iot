FROM python:3.10 AS base

ENV CODE=/code
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

COPY ["requirements.txt", "/tmp/"]

RUN apt-get update && \
        apt-get -y install gcc make git curl && \
        apt-get clean && \
        apt-get autoclean && \
        rm -rf /var/lib/apt/lists/*

COPY . $CODE

RUN pip3 install -r /tmp/requirements.txt

WORKDIR $CODE