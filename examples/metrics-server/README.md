# Сервер Prometheus

## Как запустить?

* Создать сеть, если еще не сделали этого, следуя инструкции из `metrics-client/README.md`:
```sh
docker network create example-network
```

* Собрать докер образ:
```sh
./build.sh
```

* Запустить докер контейнер:
```
docker run --network example-network --rm -p 9090:9090 qemu-riscv-cluster/metrics-server
```

Теперь можно открыть фронтенд Prometheus'а в браузере: `localhost:9090`. Кастомная метрика называется `custom_fields_field_1`. Из дефолтных метрик интересуют `cpu_usage_user` и `mem_used`.
