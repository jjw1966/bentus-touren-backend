# 🟩 Basimage
FROM python:3.10-slim

# 🟩 Arbetskatalog
WORKDIR /app

# 🟩 Kopiera filer
COPY . .

# 🟩 Installera beroenden
RUN pip install --no-cache-dir -r requirements.txt

# 🟩 Starta FastAPI med Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
