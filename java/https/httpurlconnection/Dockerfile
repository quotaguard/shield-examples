# Start from a standard Java image
FROM eclipse-temurin:17-alpine

# Install curl
RUN apk add --no-cache curl

WORKDIR /app

# Copy Java file into the container
COPY HttpsTest.java .

# Fetch and unpack QGPass
RUN curl -sSL https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz \
  | tar xz -C /app/

# Compile Java class
RUN javac HttpsTest.java

# Run Java app behind QGPass
CMD ["bin/qgpass", "java", "HttpsTest"]
