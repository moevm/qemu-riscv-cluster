FROM alpine:3.21

RUN apk update && apk add telegraf
COPY . .

ENTRYPOINT [ "telegraf", "--config", "telegraf.conf" ]
