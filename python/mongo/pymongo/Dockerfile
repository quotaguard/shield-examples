# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir pymongo

# Download and extract QGTunnel software
RUN curl https://s3.amazonaws.com/quotaguard/qgtunnel-latest.tar.gz | tar xz

ENV QGTUNNEL_DEBUG=true

# Command to run when the container starts, assuming the environment variable is passed at runtime
CMD ["bin/qgtunnel", "python", "app.py"]
