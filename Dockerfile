# Use Python 3.10-slim (Matches your README requirement)
FROM python:3.10-slim

# Install system dependencies required for XGBoost (OpenMP)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application structure
# This includes app.py, services/, model/, data/, static/, and templates/
COPY . .

# Expose the port Flask usually runs on
EXPOSE 5000

# Use Gunicorn to serve the app (Production server)
# -w 2: uses 2 worker processes (good for low-power NAS)
# -b 0.0.0.0:5000: binds to all interfaces
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]