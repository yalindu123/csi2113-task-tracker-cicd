# --- Base image ---
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Flask runs on port 5000
EXPOSE 5000

# Basic healthcheck so `docker ps` / compose can report container health
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

# Run with a production-ready server (gunicorn) instead of the Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
