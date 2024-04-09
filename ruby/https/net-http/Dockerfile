FROM ruby:latest

WORKDIR /app/

RUN gem install net-http

# Download and extract qgpass
RUN curl https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz -C /app/

COPY net-http.rb net-http.rb

ENTRYPOINT [ "/app/bin/qgpass", "ruby", "net-http.rb" ]