FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --root-user-action=ignore -r requirements.txt

COPY . /app

CMD ["python", "server.py"]
