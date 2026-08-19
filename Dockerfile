FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --root-user-action=ignore \
    httpx starlette uvicorn \
    ./packages/markitdown \
    ./packages/markitdown-mcp

CMD ["python", "server.py"]
