FROM elixir:latest

COPY . /app/

WORKDIR /app/

RUN mix local.hex --force && \
    mix deps.get && \
    curl https://s3.amazonaws.com/quotaguard/qgpass-latest.tar.gz | tar xz

ENTRYPOINT [ "/app/bin/qgpass", "mix", "run", "-e", "Qg.request_ip()" ]
