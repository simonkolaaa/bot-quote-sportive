FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

# Imposta fuso orario di default a Roma
ENV TZ="Europe/Rome"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Il comando python usa -u per forzare unbuffered output e vedere i log in tempo reale
CMD ["python", "-u", "scheduler.py"]
