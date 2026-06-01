# Apache HttpClient 5 HTTPS Proxy Example for QuotaGuard Shield
FROM eclipse-temurin:17-alpine

RUN apk add --no-cache curl wget

WORKDIR /app

# Apache HttpClient 5 + transitive deps
RUN wget -q https://repo1.maven.org/maven2/org/apache/httpcomponents/client5/httpclient5/5.3.1/httpclient5-5.3.1.jar -O httpclient5.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/httpcomponents/core5/httpcore5/5.2.4/httpcore5-5.2.4.jar -O httpcore5.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/httpcomponents/core5/httpcore5-h2/5.2.4/httpcore5-h2-5.2.4.jar -O httpcore5-h2.jar && \
    wget -q https://repo1.maven.org/maven2/commons-codec/commons-codec/1.17.0/commons-codec-1.17.0.jar -O commons-codec.jar && \
    wget -q https://repo1.maven.org/maven2/org/slf4j/slf4j-api/2.0.13/slf4j-api-2.0.13.jar -O slf4j-api.jar && \
    wget -q https://repo1.maven.org/maven2/org/slf4j/slf4j-nop/2.0.13/slf4j-nop-2.0.13.jar -O slf4j-nop.jar

COPY HttpsTest.java .

# QGPass is required: it terminates TLS to the Shield proxy and adds auth.
RUN curl -sSL https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz -C /app/

ENV CLASSPATH=".:httpclient5.jar:httpcore5.jar:httpcore5-h2.jar:commons-codec.jar:slf4j-api.jar:slf4j-nop.jar"

RUN javac -cp "$CLASSPATH" HttpsTest.java

CMD ["bin/qgpass", "java", "HttpsTest"]
