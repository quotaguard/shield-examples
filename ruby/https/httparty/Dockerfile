# Use official Ruby image
FROM ruby:latest

# Install required gems
RUN gem install httparty

# Create a working directory in the container
WORKDIR /app

# Download and extract qgpass
RUN curl https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz -C /app/

# Copy the Ruby script into the container
COPY app.rb .

# Run our script through qgpass
CMD [ "/app/bin/qgpass", "ruby", "app.rb" ]