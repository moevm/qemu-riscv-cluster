FROM alpine:3.21

RUN apk update && apk add prometheus
COPY . .

ENTRYPOINT [ "prometheus" ]
