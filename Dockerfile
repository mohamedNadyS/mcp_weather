FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Simple command that works
CMD ["python", "-m", "uvicorn", "mcp_weather.server:app", "--host", "0.0.0.0", "--port", "8000"]