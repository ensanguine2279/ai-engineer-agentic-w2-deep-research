FROM python:3.11-slim

# Prevents Python from writing .pyc files and buffers stdout (cleaner Cloud Run logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first so Docker can cache this layer across builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Cloud Run injects PORT at runtime (defaults to 8080); app.py reads this env var
ENV PORT=8080
EXPOSE 8080

CMD ["python", "app.py"]
