# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy backend app files
COPY backend/ /app/

# Copy models from project root to container
COPY models/ /models/

# Install required packages
RUN pip install --no-cache-dir fastapi uvicorn pandas scikit-learn joblib

# Run the backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
