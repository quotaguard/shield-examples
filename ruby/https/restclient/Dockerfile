FROM ruby:latest

WORKDIR /app/

RUN gem install rest-client

# Download and extract qgpass
RUN curl https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz -C /app/

COPY restclient.rb restclient.rb

ENTRYPOINT [ "/app/bin/qgpass", "ruby", "restclient.rb" ]