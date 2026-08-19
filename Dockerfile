FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --root-user-action=ignore \
    httpx starlette uvicorn \
    ./packages/markitdown \
    ./packages/markitdown-mcp

RUN sed -i 's/stateless=True/stateless=False/' /usr/local/lib/python3.13/site-packages/markitdown_mcp/__main__.py

CMD ["python", "server.py"]
