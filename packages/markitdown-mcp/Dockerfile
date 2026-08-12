FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV MARKITDOWN_ENABLE_PLUGINS=True

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install \
    /app/packages/markitdown \
    /app/packages/markitdown-mcp

WORKDIR /workdir

ARG USERID=nobody
ARG GROUPID=nogroup

USER $USERID:$GROUPID

ENTRYPOINT ["markitdown-mcp"]
