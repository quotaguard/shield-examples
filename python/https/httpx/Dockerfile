FROM python:latest

WORKDIR /app

# Install dependencies
RUN pip install httpx

# Copy app code
COPY app.py .

# Set the default command
CMD ["python", "app.py"]
