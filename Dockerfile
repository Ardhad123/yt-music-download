# Python 3.11 base image
FROM python:3.11-slim

# YAHAN CHANGE KIYA HAI: ffmpeg ke sath 'nodejs' bhi install kar rahe hain
RUN apt-get update && apt-get install -y ffmpeg nodejs

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Start the server using gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:10000", "app:app"]
