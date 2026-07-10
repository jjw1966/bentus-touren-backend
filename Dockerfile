# 1. Stabil Python-version
FROM python:3.10-slim

# 2. Installera systempaket som pandas/numpy behöver
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Arbetskatalog
WORKDIR /app

# 4. Kopiera hela projektet (viktigt!)
COPY . .

# 5. Installera Python-paket
RUN pip install --no-cache-dir -r requirements.txt

# 6. Exponera porten backend lyssnar på
EXPOSE 10000

# 7. Starta Gunicorn och kör main.py
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]
