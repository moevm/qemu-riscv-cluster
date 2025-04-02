FROM alpine:3.21 as base

RUN apk update && apk upgrade

FROM base as alpine_replicated_nodes

RUN apk add python3

COPY ../src/ping.py ping.py

ENTRYPOINT [ "python", "ping.py" ]

FROM base as alpine_central_node

RUN apk add tcpdump

RUN mkdir /logs

COPY ../src/entrypoint.sh entrypoint.sh

ENTRYPOINT [ "sh", "entrypoint.sh" ]
