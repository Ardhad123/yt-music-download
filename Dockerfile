# Yahan humne Python 3.9 ko 3.11 se upgrade kar diya hai
FROM python:3.11-slim

# Install FFmpeg (Required for audio extraction)
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Start the server using gunicorn (1 worker for free tier)
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:10000", "app:app"]
