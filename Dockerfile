# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# If you ever need system deps for native builds, uncomment below
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential libpq-dev \
#  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the source code
COPY . .

ENV FLASK_APP=app
# Default container port; can be overridden by passing -e PORT=xxxx
ENV PORT=8000

EXPOSE 8000

# Use sh -c so ${PORT} is expanded at runtime
CMD ["sh", "-c", "exec gunicorn 'app:create_app()' --bind 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile -"]
