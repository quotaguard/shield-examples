FROM python:latest

#install paramiko
RUN pip install -U pip && \
    pip install paramiko

WORKDIR /app

#install qgtunnel
RUN curl https://s3.amazonaws.com/quotaguard/qgtunnel-latest.tar.gz | tar xz
ENV QGTUNNEL_DEBUG true

COPY .qgtunnel .qgtunnel
COPY app.py app.py
COPY .run.sh .run.sh

ENTRYPOINT [ "/bin/bash", "/app/.run.sh" ]

