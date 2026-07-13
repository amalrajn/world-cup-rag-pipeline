# Container image for the World Cup RAG Gradio app (Google Cloud Run).
FROM python:3.10-slim

WORKDIR /app

# Install dependencies first so this layer is cached across code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and documents.
COPY . .

# Cloud Run injects the PORT env var (default 8080); app.py binds to it.
ENV PORT=8080

CMD ["python", "app.py"]
