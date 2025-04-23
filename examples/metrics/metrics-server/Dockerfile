FROM alpine:3.21

RUN apk update && apk add prometheus pushgateway
COPY . .

EXPOSE 9091

ENTRYPOINT [ "sh", "entry.sh" ]
