# Use a slim official Python image for smaller size
# FROM python:3.13-slim
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create the app directory
WORKDIR /app

# Install system dependencies (if needed, e.g. for psycopg2)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     libpq-dev && \
#     rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies in one step to leverage caching
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional, for production)
# RUN --mount=type=cache,target=/root/.cache \
#     python manage.py collectstatic --noinput

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

# Expose the port the app runs on
EXPOSE 8000

VOLUME ["/app/logs/"]

# Use Gunicorn for production
CMD ["gunicorn", "TemplateService.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
