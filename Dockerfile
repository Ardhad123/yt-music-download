FROM python:3.11-slim

# Install ffmpeg, curl aur unzip (Deno ke liye zaroori)
RUN apt-get update && apt-get install -y ffmpeg curl unzip

# Deno JS Engine install karna
RUN curl -fsSL https://deno.land/x/install/install.sh | sh
ENV PATH="/root/.deno/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Start the server using gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:10000", "app:app"]
