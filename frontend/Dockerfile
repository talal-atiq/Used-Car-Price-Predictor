# frontend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Copy frontend code and requirements
COPY frontend/ /app/
COPY frontend/requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the Streamlit frontend
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
