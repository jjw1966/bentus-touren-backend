# Använd stabil Python-version
FROM python:3.10-slim

# Installera systempaket som pandas behöver
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Skapa arbetsmapp
WORKDIR /app

# Kopiera projektfiler
COPY requirements.txt .
COPY main.py .
COPY Procfile .

# Installera Python-paket
RUN pip install --no-cache-dir -r requirements.txt

# Exponera porten Flask kör på
EXPOSE 10000

# Starta gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]
