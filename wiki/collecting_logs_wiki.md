# Инструменты для сбора логов 

## Необходимый стек:
  - [Сбор логов](#сбор-логов)
  - [Хранилище логов](#хранилище-логов)
  - [Визуализация и анализ логов](#визуализация-и-анализ-логов)

## Сбор логов
- **[Fluent Bit](https://github.com/fluent/fluent-bit/releases)**
  * поддержка архитекутры RISC-V (были трудности с версией [LuaJIT](https://chronosphere.io/learn/fluent-bit-risc-v/), возможно до сих пор существуют)
  *  Совместимость с Prometheus и OpenTelemetry.
  *  Написан на C.
  *  Fluent Bit поддерживает множество плагинов для сбора, обработки и отправки данных.
  *  Поддержка проекта, Last Version v3.2.8, Released On Mar 04, 2025, 6.6к звезд.
  *    Apache License Version 2.0, January 2004
- **[Fluentd](https://github.com/fluent/fluentd)**
    * Более мощный аналог Fluent Bit.
    * Требует больше ресурсов, чем Fluent Bit, но подходит для сложных сценариев.
- **[rsyslog](https://github.com/rsyslog/rsyslog.git)**
    * Классический сборщик логов, использующий протокол Syslog.
    * Написан на С.
    * Последний релиз December 6, 2022; 2 years ago.
- **[syslog-ng](https://github.com/syslog-ng/syslog-ng)**
    * Альтернатива rsyslog с более гибкой конфигурацией.
    * Поддерживает множество форматов и протоколов.

## Хранилище логов
- **[Elasticsearch](https://github.com/elastic/elasticsearch)**
    * Интеграция с Fluent Bit через плагин elasticsearch
    * Подходит для хранения и индексации больших объемов логов.
    * Высокопроизводительная поисковая и аналитическая система.
- **[Loki](https://github.com/grafana/loki)**
    * Легковесное хранилище логов, оптимизированное для работы с метками (labels).
    * Потребляет меньше ресурсов, чем Elasticsearch.
    * Интеграция с Fluent Bit через плагин loki.
    * Тесная интеграция с Grafana.
    * AGPL-3.0 license
## Визуализация и анализ логов
- **[Kibana](https://github.com/elastic/kibana)**
    * Визуализация и анализ данных, хранящихся в Elasticsearch
    * Поддерживает сложные запросы, дашборды и алерты.
    * В основном Elasticsearch.
    * Часть экосистемы ELK (Elasticsearch, Logstash, Kibana).
- **[Grafana](https://github.com/grafana/grafana)**
    * Универсальный инструмент для визуализации данных.
    * Подходит для работы с Loki, Elasticsearch, Prometheus и другими источниками данных.
    * Позволяет создавать дашборды и настраивать алерты.
    * Множество источников (Prometheus, Loki, Elasticsearch, Graphite, InfluxDB и т.д.).
    * Часть экосистемы Grafana (Prometheus, Loki, Tempo).

