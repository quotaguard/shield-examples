# Start from a standard Debian-based image
FROM openjdk:17-slim

# Install curl just in case
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Java file into the container
COPY HttpsTest.java .

# Fetch and unpack QGPass
RUN curl -sSL https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz \
  | tar xz -C /app/

# Compile Java class
RUN javac HttpsTest.java

# Default command: run Java app behind QGPass
CMD ["bin/qgpass", "java", "HttpsTest"]
