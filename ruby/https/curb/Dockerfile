# Dockerfile
FROM ruby:latest

WORKDIR /app

# Install curb gem (it has native extensions, so build-essential is needed)
RUN apt-get update && apt-get install -y build-essential libcurl4-openssl-dev \
  && gem install curb --no-document

COPY app.rb /app/app.rb

CMD ["ruby", "app.rb"]
