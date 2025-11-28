# OkHttp HTTPS Proxy Example
FROM eclipse-temurin:17-alpine

# Install curl and wget
RUN apk add --no-cache curl wget

WORKDIR /app

# Download OkHttp JAR and its dependencies
RUN wget https://repo1.maven.org/maven2/com/squareup/okhttp3/okhttp/4.12.0/okhttp-4.12.0.jar -O okhttp.jar && \
    wget https://repo1.maven.org/maven2/com/squareup/okio/okio-jvm/3.6.0/okio-jvm-3.6.0.jar -O okio.jar && \
    wget https://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/1.8.21/kotlin-stdlib-1.8.21.jar -O kotlin-stdlib.jar && \
    wget https://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib-common/1.8.21/kotlin-stdlib-common-1.8.21.jar -O kotlin-stdlib-common.jar && \
    wget https://repo1.maven.org/maven2/org/jetbrains/annotations/13.0/annotations-13.0.jar -O annotations.jar

# Copy Java file
COPY HttpsTest.java .

# Fetch and unpack QGPass (required for QuotaGuard Shield)
RUN curl -sSL https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz -C /app/

# Set classpath environment variable for cleaner command
ENV CLASSPATH=".:okhttp.jar:okio.jar:kotlin-stdlib.jar:kotlin-stdlib-common.jar:annotations.jar"

# Compile Java class
RUN javac -cp "$CLASSPATH" HttpsTest.java

# Run with QGPass (required for QuotaGuard Shield)
CMD ["bin/qgpass", "java", "HttpsTest"]
