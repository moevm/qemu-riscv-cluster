# Клиент для сбора метрик (Telegraf)

Собирает базовые метрики (процессорное время и память), а также кастомную метрику `custom-metric.sh`. Она ничего не замеряет, просто вычисляет функцию синуса от текущего времени.

## Как запускать?

В реальных условиях клиенты-сборщики будут запущены на разных машинах с разными ip-адресами, но в демонстративных целях запустим несколько клиентов на одной машине:

* Создать сеть:
```sh
docker network create example-network
```

* Собрать докер образ:
```sh
./build.sh
```

* Запустить докер контейнер первого клиента:
```sh
docker run --network example-network --name client1 --rm -d qemu-riscv-cluster/metrics-clinet
```

* Запустить докер контейнер второго клиента:

```sh
docker run --network example-network --name client2 --rm -d qemu-riscv-cluster/metrics-clinet
```
