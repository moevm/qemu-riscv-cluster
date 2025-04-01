FROM alpine:3.21

RUN apk update && apk add cmake make gcc g++ libcurl curl-dev

WORKDIR /app

COPY scripts/get-prometheus-cpp.sh scripts/
RUN sh scripts/get-prometheus-cpp.sh

COPY . .
RUN sh scripts/build-daemon.sh

ENTRYPOINT [ "build/daemon" ]
