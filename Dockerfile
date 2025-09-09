# Dockerfile for Contextual Reasoning AI API, CLI, GUI
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY contextual_reasoning_ai/ /app/contextual_reasoning_ai/
COPY contextual_reasoning_ai/main_cli.py /app/
COPY contextual_reasoning_ai/main_gui.py /app/
COPY entrypoint.sh /app/

# Install Python dependencies
COPY contextual_reasoning_ai/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install main dependencies explicitly (for safety)
RUN pip install --no-cache-dir fastapi uvicorn pydantic numpy pillow neo4j psycopg2-binary

# Copy environment variables file
COPY contextual_reasoning_ai/.env /app/

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose API port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
