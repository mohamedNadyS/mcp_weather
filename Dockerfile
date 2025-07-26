FROM python:3.9-slim

WORKDIR /app
RUN pip install fastapi uvicorn requests python-multipart
COPY app.py .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]