FROM ruby:latest

WORKDIR /app/

RUN gem install net-sftp

#install qgtunnel
RUN curl https://s3.amazonaws.com/quotaguard/qgtunnel-latest.tar.gz | tar xz
ENV QGTUNNEL_DEBUG true

COPY sftp.rb sftp.rb
COPY qgtunnel_config .qgtunnel

ENTRYPOINT [ "bin/qgtunnel", "ruby", "sftp.rb" ]
