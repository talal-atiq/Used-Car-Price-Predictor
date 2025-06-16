# frontend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy frontend code
COPY frontend/ /app/

# Install dependencies
RUN pip install --no-cache-dir streamlit pandas scikit-learn joblib plotly

# Run the frontend
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
