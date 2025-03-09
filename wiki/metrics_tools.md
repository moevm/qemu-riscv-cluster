# Инструменты для мониторинга состояния узла

* [collectd](https://www.collectd.org/)
  - Последний релиз в 2020, последний мердж в мастер 3 недели назад (вроде живой), 3.2k звёзд.
  - collectd: MIT Licence. Плагины в основном GNU GPL и MIT LICENCE
  - Демон, собирающий метрики. Совместим с различными "фронт-ендами". В их числе, например, совместимость с Prometheus через плагин [Plugin-Write-Prometheus](https://github.com/collectd/collectd/wiki/Plugin-Write-Prometheus), который запускает обработчик запросов Prometheus'а на порту 9103 (или на любом другом, указанном в конфиге).
  - Для разных метрик надо подключать разные плагины. Основные плагины: LogFile (Writes log messages to a file or standard output), SysLog (Writes debug and status information to syslog), RRDtool (Writes data to RRD files), CSV (Writes data to CSV files), CPU (Collects CPU usage), Memory (Collects memory usage), Interface (Collects traffic of network interfaces).
  - [Плагинов](https://github.com/collectd/collectd/wiki/Table-of-Plugins) порядка 100+ штук

* [Prometheus](https://prometheus.io/)
  - Проект живой.
  - Apache 2 Licence.
  - Сервер = База данных + веб-визуализация.
  - Есть официальный [клиент для Python](https://prometheus.github.io/client_python/), неофициальные для C/C++. Можно собирать свои кастомные метрики.
  - Есть готовый докер-образ. Альтернативно, установка "FROM ubuntu" [несложная](https://github.com/jcdkiki/prometheus-example).
  
* [beszel](https://github.com/henrygd/beszel)
  - Проект живой. 9.7k звёзд на Github.
  - MIT Licence
  - Рекламирует себя как "Lightweight".
  - Есть свой клиент (демон для сборки метрик), который поддерживает метрики: CPU usage, Memory usage, Disk usage, Disk I/O, Network usage, Temperature, GPU usage / temperature / power draw - Nvidia and AMD only.
  - Легко устанавливается и настраивается https://beszel.dev/guide/getting-started

* [munin](https://github.com/munin-monitoring/munin?tab=readme-ov-file)
  - Последний релиз 2023, последний мердж в мастер 3 недели назад (проект вроде живой). 2k звёзд.
  - GNU GPL.
  - Имеет свой протокол, несовместимый с Prometheus, Graphite, etc...
  - Очень просто [установить и настроить](https://interface31.ru/tech_it/2023/01/ustanavlivaem-i-nastraivaem-sistemu-monitoringa-munin.html).
  - Много [плагинов](https://gallery.munin-monitoring.org/). Можно писать свои плагины для кастомных метрик.
  - Веб-интерфейс минималистичный.

* CollectD + StatsD + Carbon + Graphite-web
  - Проекты живые, Apache 2.0 Licence
  - Сборщик метрик на конкретном узле + Сборшик метрик со всех узлов + хранилище метрик + веб-визуализация.
  - В качестве сборщика метрик можно использовать любой carbon-совместимый сборщик, не обязательно collectd. В качестве визуализации тоже не обязательно Graphite-web. Полный список совместимых [сборщиков и веб-фронтендов](https://graphite.readthedocs.io/en/0.9.11/tools.html). Выглядит как дело вкуса, особой разницы между ними, скорее всего, нет.
  - Настроить понятное дело это всё сложнее, чем "практически" готовые решения типа описанных выше.

* [Zabbix](https://github.com/zabbix/zabbix)
  - Живой, 4.7k звёзд.
  - AGPL 3.0 Licence.
  - Веб-интерфейс + демоны на узлах кластера.
  - На первый взгляд процесс установки и настройки непонятный.
  - [Поддерживаемые метрики](https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/zabbix_agent)

