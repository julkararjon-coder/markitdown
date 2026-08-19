FROM python:3.13-slim-bullseye
ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV MARKITDOWN_ENABLE_PLUGINS=True
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool
RUN rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install \
    /app/packages/markitdown \
    /app/packages/markitdown-mcp \
    starlette httpx uvicorn
ARG USERID=nobody
ARG GROUPID=nogroup
USER $USERID:$GROUPID
EXPOSE 10000
CMD ["python", "server.py"]
