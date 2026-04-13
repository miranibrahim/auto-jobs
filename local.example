# Python base image
FROM python:3.11-slim

# Work directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run script
CMD ["python", "app.py"]