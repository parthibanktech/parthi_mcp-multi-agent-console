# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# (build-essential is often needed for python packages, curl for healthchecks if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make the start script executable
RUN chmod +x start.sh

# Define environment variable for Streamlit to work with Render
# Render provides the PORT variable, but we can set a default for local testing
ENV PORT=8501

# Run start.sh when the container launches
CMD ["./start.sh"]
