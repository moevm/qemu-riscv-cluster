# Tools for collecting logs

## Required stack:
  - [Implementing Log Collection: Sending Data from PUnit](#implementing-log-collection-sending-data-from-punit)
  - [Log collection](#log-collection)
  - [Log storage](#log-storage)
  - [Log visualization and analysis](#log-visualization-and-analysis)
  - [Stack example](#stack-example)

## Implementing Log Collection: Sending Data from PUnit

To organize the collection of logs from PUnit in a Docker container, it is necessary to set up a logging mechanism that will send data to the system for collecting, storing and visualizing logs.

Adding a Logging Driver to a Docker Container
To send logs from PUnit, you need to configure a logging driver in the Docker container. Docker supports several logging drivers that can be used to send logs to different systems. The main drivers are:
- Driver json-file
  - This is the standard Docker logging driver.
  - Logs are written to files on the host in JSON format.
  - Example of configuration in docker-compose.yml:
```
services:
  punit:
    image: punit-image
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```
- Driver fluentd
  - Sends logs directly to Fluentd or Fluent Bit.
  - Suitable for centralized log collection.
  - Can work both via TCP.
  - Example of configuration in docker-compose.yml:
```
services:
  app:
    image: docker-image
    logging:
      driver: "fluentd"
      options:
        fluentd-address: localhost:24224
        tag: app.logs
```

## Log collection
- **[Fluent Bit](https://github.com/fluent/fluent-bit/releases)**
    * RISC-V architecture support (there were some issues with [LuaJIT](https://chronosphere.io/learn/fluent-bit-risc-v/) version, maybe they still exist)
    * Compatibility with Prometheus and OpenTelemetry.
    * Written in C.
    * Fluent Bit supports many plugins for collecting, processing and sending data.
    * Project support, Last Version v3.2.8, Released On Mar 04, 2025, 6.6k stars.
    * Apache License Version 2.0, January 2004
- **[Fluentd](https://github.com/fluent/fluentd)**
    * A more powerful analogue of Fluent Bit.
    * Requires more resources than Fluent Bit, but is suitable for complex scenarios.
- **[rsyslog](https://github.com/rsyslog/rsyslog.git)**
    * Classic log collector using Syslog protocol.
    * Written in C.
    * Latest release December 6, 2022; 2 years ago.
- **[syslog-ng](https://github.com/syslog-ng/syslog-ng)**
    * Alternative to rsyslog with more flexible configuration.
    * Supports many formats and protocols.

## Log storage
- **[Elasticsearch](https://github.com/elastic/elasticsearch)**
    * Fluent Bit integration via elasticsearch plugin
    * Suitable for storing and indexing large volumes of logs.
    * High-performance search and analytics system.
- **[Loki](https://github.com/grafana/loki)**
    * Lightweight log storage optimized for working with labels.
    * Consumes fewer resources than Elasticsearch.
    * Fluent Bit integration via loki plugin.
    * Tight integration with Grafana.
    * AGPL-3.0 license
## Log visualization and analysis
- **[Kibana](https://github.com/elastic/kibana)**
    * Visualization and analysis of data stored in Elasticsearch
    * Supports complex queries, dashboards, and alerts.
    * Mostly Elasticsearch.
    * Part of the ELK ecosystem (Elasticsearch, Logstash, Kibana).
- **[Grafana](https://github.com/grafana/grafana)**
    * Universal data visualization tool.
    * Suitable for working with Loki, Elasticsearch, Prometheus and other data sources.
    * Allows you to create dashboards and set up alerts.
    * Multiple sources (Prometheus, Loki, Elasticsearch, Graphite, InfluxDB, etc.).
    * Part of the Grafana ecosystem (Prometheus, Loki, Tempo).


## Stack example
- Fluent Bit + Loki + Grafana
  configure the PUnit driver to send to Fluent Bit. Configure Fluent Bit (Fluent Bit will receive logs from PUnit and send them to an external Loki). Sending data from Fluent Bit to Loki. Connecting Grafana to Loki for log visualization.