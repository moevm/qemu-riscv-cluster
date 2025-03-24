FROM alpine:3.21

RUN apk update && apk add cmake make gcc g++

WORKDIR /app
COPY . .
RUN sh scripts/get-prometheus-cpp.sh
RUN sh scripts/build-daemon.sh

ENTRYPOINT [ "build/daemon" ]
