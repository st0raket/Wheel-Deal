# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /model

# Copy the requirements file into the container
COPY requirements.txt /model/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . /model/

# Expose the port that your application will run on
EXPOSE 5000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "5000"]
