# Tools for monitoring working units' state.

* [collectd](https://www.collectd.org/)
  - Last release in 2020, last merge to master 3 weeks ago (project seems to be alive), 3.2k stars.
  - collectd: MIT Licence. Plugins are mostly GNU GPL and MIT LICENCE.
  - Daemon that collects metrics. Compatible with various "front-ends". For example, compatibility with Prometheus via [Plugin-Write-Prometheus](https://github.com/collectd/collectd/wiki/Plugin-Write-Prometheus) plugin, which runs the Prometheus request handler on port 9103 (or any other specified in the config).
  - Different plugins need to be connected for different metrics. Main plugins: LogFile (Writes log messages to a file or standard output), SysLog (Writes debug and status information to syslog), RRDtool (Writes data to RRD files), CSV (Writes data to CSV files), CPU (Collects CPU usage), Memory (Collects memory usage), Interface (Collects traffic of network interfaces).
  - 100+ [plugins](https://github.com/collectd/collectd/wiki/Table-of-Plugins).

* [Prometheus](https://prometheus.io/)
  - Alive
  - Apache 2 Licence.
  - Server = Database + Web-frontend.
  - There is an official [client for Python](https://prometheus.github.io/client_python/), unofficial for C/C++. Can collect your own custom metrics.
  - There is a "Prometheus" docker image availible. Alternatively, "FROM ubuntu" installation is [simple](https://github.com/jcdkiki/prometheus-example).
  
* [beszel](https://github.com/henrygd/beszel)
  - Alive. 9.7k stars on Github.
  - MIT Licence
  - Advertises itself as "Lightweight".
  - There is a client (deamon that collects metrics), which supports metrics: CPU usage, Memory usage, Disk usage, Disk I/O, Network usage, Temperature, GPU usage / temperature / power draw - Nvidia and AMD only.
  - Easy to install and configure: https://beszel.dev/guide/getting-started

* [munin](https://github.com/munin-monitoring/munin?tab=readme-ov-file)
  - Last release in 2023, last merge in master 3 weeks ago (project seems to be alive). 2k stars.
  - GNU GPL.
  - Has its own protocol, incompatible with Prometheus, Graphite, etc...
  - Easy to [install and configure](https://interface31.ru/tech_it/2023/01/ustanavlivaem-i-nastraivaem-sistemu-monitoringa-munin.html).
  - Lots of [plugins](https://gallery.munin-monitoring.org/). You can write your own plugins for collecting custom metrics.
  - Minimalisted web interface.

* CollectD + StatsD + Carbon + Graphite-web
  - Alive, Apache 2.0 Licence
  - Metrics collector (on each node) + Metrics collector (recieves metrics from nodes) + metrics storage + web visualization.
  - You can use any carbon-compatible metrics collector instead of collectd. For visualization you can use something different from Graphite-web. Here is a full list of all [collectors and web-frontends](https://graphite.readthedocs.io/en/0.9.11/tools.html) compatible with carbon. Looks like a matter of taste, there is most likely no special difference between them.
  - Obviously, it is more difficult to configure than "almost" ready-made solutions like those described above.

* [Zabbix](https://github.com/zabbix/zabbix)
  - Alive, 4.7k stars.
  - AGPL 3.0 Licence.
  - Web interface + daemons for collecting metrics.
  - At first glance, the installation and configuration process is weird.
  - List of [supported metrics](https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/zabbix_agent)

