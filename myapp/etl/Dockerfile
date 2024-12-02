FROM python:3.10-slim-bullseye

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /etl

# Set PYTHONPATH for module resolution
ENV PYTHONPATH=/etl

# Copy requirements file and install dependencies
COPY requirements.txt . 
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 3000
EXPOSE 3000

# Command to run the python file
CMD ["python", "etl.py"]
