FROM python:3.12.5-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Run migrations, collect static files, and start server with gunicorn
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn TemplateService.wsgi --bind 0.0.0.0:8080 --workers 3 --worker-class sync --timeout 300 --keep-alive 75 --max-requests 1000 --max-requests-jitter 100 --access-logfile - --error-logfile -