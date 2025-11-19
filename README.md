# 📊 MikroTik Observability Stack

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![CI](https://github.com/ranas-mukminov/mikrotik-observability-stack/actions/workflows/ci.yml/badge.svg)](https://github.com/ranas-mukminov/mikrotik-observability-stack/actions/workflows/ci.yml)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-ready-2496ED?logo=docker)](https://docs.docker.com/compose/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-326ce5?logo=kubernetes)](https://kubernetes.io/)

Self-hosted observability for MikroTik RouterOS: metrics, logs, and dashboards in minutes.

**Production-ready** | **Docker & Kubernetes** | **Pre-configured Dashboards** | **MikroTik RouterOS**

> ⚡ **[Quick Start](#-quick-start-in-3-commands--быстрый-старт-за-3-команды)** | 📖 **[Documentation](#-documentation--документация)** | 🎨 **[Dashboards](#-pre-configured-dashboards--готовые-дашборды)** | 🔧 **[Profiles](#-deployment-options--варианты-развёртывания)** | 💼 **[Professional Services](#-production-deployment--professional-support)**

---

## English

### 📑 Table of Contents

- [Why This Project](#why-this-project)
- [Features](#-features--возможности)
- [Quick Start in 3 Commands](#-quick-start-in-3-commands--быстрый-старт-за-3-команды)
- [Architecture Overview](#architecture-overview)
- [Deployment Options](#-deployment-options--варианты-развёртывания)
- [Pre-configured Dashboards](#-pre-configured-dashboards--готовые-дашборды)
- [Configuration](#configuration)
- [Testing and Validation](#testing-and-validation)
- [Troubleshooting](#-troubleshooting--решение-проблем)
- [Security and Performance](#security-and-performance)
- [Legal / Responsible Use](#legal--responsible-use)
- [Production Deployment & Professional Support](#-production-deployment--professional-support)
- [Author & Professional Services](#-author--professional-services)
- [Support](#-support--поддержка)
- [Documentation](#-documentation--документация)
- [Contributing](#contributing)
- [License](#license)

### Why this project

MikroTik routers power countless SMB networks, ISPs, and homelabs, yet teams still glue together Prometheus, Grafana, and exporters manually. This repository delivers an opinionated, vendor-neutral stack that focuses on RouterOS nuances while staying extensible for future needs. Everything lives in source control, so you can audit, customize, and redeploy confidently.

---

### 🎯 Production Deployment & Professional Support

Looking for **production-grade MikroTik monitoring** or **professional DevOps assistance**?

**[run-as-daemon.ru](https://run-as-daemon.ru)** — Professional DevOps & Monitoring Services

**Services:**
- 📊 **Network Monitoring**: Complete MikroTik observability stack deployment
- 🔍 **Custom Dashboards**: Tailored Grafana dashboards for your infrastructure
- 🏗️ **Infrastructure Design**: Scalable monitoring architecture (Docker, Kubernetes, Nomad)
- 🔒 **Security-First**: Secure exporters, authentication, encrypted communications
- ⚙️ **Integration**: Connect with existing monitoring systems (Zabbix, PRTG, etc.)
- 📈 **Performance Optimization**: Prometheus tuning, efficient scraping, retention policies
- 🤖 **Automation**: Ansible playbooks, Infrastructure as Code
- 🚨 **Alerting**: Smart alert rules, integration with PagerDuty, Slack, Teams

💬 **Contact for consulting**: Telegram, VK, WhatsApp, GitHub

---

## ✨ Features / Возможности

### English:
- 📊 **Complete Observability**: Metrics (Prometheus) + Logs (Loki) + Visualization (Grafana)
- 🎨 **Pre-configured Dashboards**: WAN, CPU/RAM, VPN, QoS, Wireless, Firewall
- 🔌 **Multiple Exporters**: RouterOS API and SNMP support
- 📝 **Centralized Logging**: Syslog collection via Promtail + Loki
- 🚨 **Smart Alerting**: CPU, memory, packet loss, interface degradation alerts
- 🐳 **Docker Compose**: Quick start with minimal and full profiles
- ☸️ **Kubernetes Ready**: Production-grade manifests included
- 🔒 **Security-First**: Read-only accounts, firewall rules, encrypted connections
- 📈 **Scalable**: From homelab to ISP-scale deployments
- 🔧 **CLI Tools**: mosctl for validation and config generation

### Русский:
- 📊 **Полная наблюдаемость**: Метрики (Prometheus) + Логи (Loki) + Визуализация (Grafana)
- 🎨 **Готовые дашборды**: WAN, CPU/RAM, VPN, QoS, беспроводные, фаервол
- 🔌 **Несколько экспортёров**: Поддержка RouterOS API и SNMP
- 📝 **Централизованные логи**: Сбор syslog через Promtail + Loki
- 🚨 **Умные алерты**: CPU, память, потери пакетов, падение интерфейсов
- 🐳 **Docker Compose**: Быстрый старт с минимальным и полным профилями
- ☸️ **Готовность к Kubernetes**: Продакшн-манифесты включены
- 🔒 **Безопасность**: Read-only аккаунты, правила фаервола
- 📈 **Масштабируемость**: От домашней лаборатории до масштабов ISP
- 🔧 **CLI инструменты**: mosctl для валидации и генерации конфигов

### Architecture overview

Metrics path: MikroTik routers expose data via SNMP or RouterOS API exporters, Prometheus scrapes them, and Grafana renders dashboards and alerts.

Logs path: Routers forward syslog to Promtail which forwards structured streams into Loki for querying inside Grafana.

```
        +-----------------+          +-----------------+
        | MikroTik Router |--API-->  | RouterOS Export |
        | (SNMP / Syslog) |--SNMP->  |   or SNMP Expo  |
        |                 |--Syslog->| Promtail        |
        +-----------------+          +-----------------+
                 \                         /
                  \                       /
                 Metrics ------------ Logs
                       \             /
                        \           /
                         v         v
                      Prometheus  Loki
                           \       /
                            \     /
                              Grafana
```

## 🎯 Quick Start in 3 Commands / Быстрый старт за 3 команды

### English:
```bash
# 1. Clone and configure
git clone https://github.com/ranas-mukminov/mikrotik-observability-stack.git && cd mikrotik-observability-stack
cp config/mikrotik-devices.example.yml config/mikrotik-devices.yml && cp config/env.example .env

# 2. Start the stack (minimal profile)
docker compose -f compose/docker-compose.minimal.yml up -d

# 3. Access Grafana
open http://localhost:3000  # Login: admin / password from .env
```

### Русский:
```bash
# 1. Клонировать и настроить
git clone https://github.com/ranas-mukminov/mikrotik-observability-stack.git && cd mikrotik-observability-stack
cp config/mikrotik-devices.example.yml config/mikrotik-devices.yml && cp config/env.example .env

# 2. Запустить стек (минимальный профиль)
docker compose -f compose/docker-compose.minimal.yml up -d

# 3. Открыть Grafana
open http://localhost:3000  # Логин: admin / пароль из .env
```

📋 **Access all services:**
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093 (full profile)

**Requirements:**
- Docker 24+ and Docker Compose plugin
- MikroTik routers with API and/or SNMP enabled
- `/system logging` rule to send syslog to the Promtail host
- Optional: GNU Make and Python 3.11+ for CLI/testing

### Configuration

`config/mikrotik-devices.yml` defines routers:

```yaml
routers:
  - name: edge-01
    address: 10.10.10.1
    exporter: routeros
    api_port: 8728
    username: monitor
    password: changeme
    labels:
      site: hq
      role: edge
  - name: ap-02
    address: 10.10.20.5
    exporter: snmp
    snmp:
      version: 2c
      community: observability
      port: 161
```

- `exporter` may be `routeros` (API-based) or `snmp`.
- Credentials are stored locally only; use secrets management in production.
- `.env` variables control Grafana admin credentials, Prometheus retention, Loki retention, and exposed ports.

## 🚀 Deployment Options / Варианты развёртывания

| Feature | Minimal | Full | Kubernetes |
|---------|---------|------|------------|
| **Prometheus** | ✅ | ✅ | ✅ |
| **Grafana** | ✅ | ✅ | ✅ |
| **RouterOS Exporter** | ✅ | ✅ | ✅ |
| **SNMP Exporter** | ❌ | ✅ | ✅ |
| **Loki** | ❌ | ✅ | ✅ |
| **Promtail** | ❌ | ✅ | ✅ |
| **Alertmanager** | ❌ | ✅ | ✅ |
| **Persistent Volumes** | ❌ | ✅ | ✅ |
| **High Availability** | ❌ | ❌ | ✅ |
| **Best For** | PoC, Labs | SMB Production | Enterprise |

**Recommendations:**
- **Minimal**: Testing, homelab, metrics-only monitoring
- **Full**: Small business production, complete observability
- **Kubernetes**: Multi-site, high availability, enterprise scale

**Start Commands:**
```bash
# Minimal profile (Prometheus + Grafana + RouterOS exporter)
docker compose -f compose/docker-compose.minimal.yml up -d

# Full profile (adds Loki, Promtail, Alertmanager, SNMP exporter)
docker compose -f compose/docker-compose.full.yml up -d

# Kubernetes (see k8s/ directory for manifests)
kubectl apply -f k8s/namespaces.yml
kubectl apply -f k8s/
```

## 🎨 Pre-configured Dashboards / Готовые дашборды

### English:
The stack includes professionally designed Grafana dashboards:

- **📡 WAN Overview**: Throughput, latency, packet loss, traffic distribution
- **💻 System Resources**: CPU, RAM, disk, temperature monitoring
- **🔌 Interfaces**: Traffic per interface, errors, status
- **🔐 VPN Tunnels**: Active connections, throughput, user statistics
- **📶 Wireless**: Client count, signal strength, channel utilization
- **⚙️ QoS Queues**: Queue utilization, dropped packets, bandwidth allocation
- **🛡️ Firewall**: Rules hits, connection tracking, NAT statistics
- **🚨 Alerts Overview**: Active alerts, alert history, notification status

### Русский:
Стек включает профессионально разработанные дашборды Grafana:

- **📡 WAN Обзор**: Пропускная способность, задержки, потери пакетов
- **💻 Системные ресурсы**: CPU, RAM, диск, температура
- **🔌 Интерфейсы**: Трафик по интерфейсам, ошибки, статус
- **🔐 VPN Туннели**: Активные подключения, пропускная способность
- **📶 Беспроводная сеть**: Количество клиентов, уровень сигнала
- **⚙️ QoS Очереди**: Использование очередей, отброшенные пакеты
- **🛡️ Фаервол**: Срабатывания правил, отслеживание соединений
- **🚨 Обзор алертов**: Активные алерты, история, статус уведомлений

## 🐛 Troubleshooting / Решение проблем

### Common Issues / Частые проблемы

#### 1. No Data in Grafana
**English**: Check Prometheus targets at http://localhost:9090/targets. Ensure your MikroTik devices are reachable and API/SNMP credentials are correct in `config/mikrotik-devices.yml`.

**Русский**: Проверьте цели Prometheus по адресу http://localhost:9090/targets. Убедитесь, что устройства MikroTik доступны и учётные данные API/SNMP верны в `config/mikrotik-devices.yml`.

#### 2. High Memory Usage
**English**: Adjust retention policies in `.env`. Reduce `PROMETHEUS_RETENTION_DAYS` or increase scrape intervals in `docker/prometheus/prometheus.yml`.

**Русский**: Настройте политики ретенции в `.env`. Уменьшите `PROMETHEUS_RETENTION_DAYS` или увеличьте интервалы опроса в `docker/prometheus/prometheus.yml`.

#### 3. Syslog Not Appearing in Loki
**English**: Verify RouterOS logging configuration points to the Promtail host. Check Promtail logs for connection errors. Ensure UDP port 1514 is open.

**Русский**: Проверьте, что настройки логирования RouterOS указывают на хост Promtail. Проверьте логи Promtail на наличие ошибок подключения. Убедитесь, что UDP порт 1514 открыт.

#### 4. Exporter Connection Refused
**English**: Check firewall rules on MikroTik devices. Ensure API (port 8728) or SNMP (port 161) is enabled and accessible. Verify read-only user accounts exist.

**Русский**: Проверьте правила фаервола на устройствах MikroTik. Убедитесь, что API (порт 8728) или SNMP (порт 161) включены и доступны. Проверьте наличие учётных записей read-only.

### Debug Commands
```bash
# Check stack status
docker compose ps

# View exporter logs
docker compose logs -f routeros-exporter

# Validate configuration
mosctl validate-config

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Test Loki query
curl -G -s "http://localhost:3100/loki/api/v1/query" --data-urlencode 'query={job="syslog"}'

# Check container resource usage
docker stats

# Restart specific service
docker compose restart prometheus
```

### Testing and validation

- Run schema checks: `scripts/validate-config.sh`.
- Run unit tests for CLI/config logic: `pytest tests/unit`.
- Run integration smoke tests (optional, requires Docker): `pytest tests/integration -m compose`.
- CLI helpers:
  - `mosctl validate-config`
  - `mosctl check-connectivity`
  - `mosctl generate-prometheus-targets`

- Create dedicated read-only MikroTik accounts for SNMP and API exporters.
- Restrict API/SNMP access via firewall address-lists; Prometheus should be the only poller.
- Adjust scrape interval and `PROMETHEUS_RETENTION_DAYS` to balance disk use vs. history.
- CI runs linting, formatting, dependency auditing, and container security scans via GitHub Actions + `scripts/security-scan.sh`.

### Security and performance

- Monitor only networks you own or are authorized to operate.
- MikroTik, RouterOS, Grafana, Prometheus, and Loki are trademarks of their respective owners; this project is unaffiliated.
- No proprietary MikroTik software or MIB files are redistributed. Provide your own RouterOS licenses.

### Legal / responsible use

## 👨‍💻 Author & Professional Services

**Ранас М. (Ranas M.)** — DevOps Engineer & Network Monitoring Specialist

### 🌐 Professional Services: [run-as-daemon.ru](https://run-as-daemon.ru)

**"Observe by design. Scale by default"** — Production-ready monitoring with performance optimization

#### 💼 Services Offered:

**📊 Monitoring & Observability**
- MikroTik observability stack deployment and tuning
- Custom Grafana dashboard development
- Prometheus optimization for large-scale networks
- Multi-site monitoring aggregation
- Integration with existing tools (Zabbix, PRTG, Nagios)

**🏗️ Infrastructure & Orchestration**
- Docker, Kubernetes, Nomad deployments
- High-availability cluster configuration
- Scalable monitoring architecture
- CI/CD integration for monitoring configs

**🔒 Security & Hardening**
- Secure exporter configuration
- Authentication and encryption setup
- Network security for monitoring systems
- Compliance and audit trails

**⚙️ Network Administration**
- MikroTik router configuration and optimization
- VPN setup (WireGuard, OpenVPN, L2TP/IPsec)
- Firewall rules and network segmentation
- Performance troubleshooting

#### 📞 Contact for Consulting:
- 🌐 Website: [run-as-daemon.ru](https://run-as-daemon.ru)
- 💬 Telegram: Contact via website
- 📱 VK: Contact via website
- 💼 WhatsApp: Contact via website
- 🐙 GitHub: [@ranas-mukminov](https://github.com/ranas-mukminov)

## 📮 Support / Поддержка

**Community Support:**
- Open an issue on [GitHub Issues](https://github.com/ranas-mukminov/mikrotik-observability-stack/issues)
- Check existing issues and discussions
- Review documentation and examples

**Professional Support:**
- Custom monitoring solutions
- Production deployment assistance
- Performance optimization consulting
- 24/7 monitoring and incident response
- Training and workshops
- Long-term maintenance contracts

Contact: [run-as-daemon.ru](https://run-as-daemon.ru)

## 📚 Documentation / Документация

- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines
- **[LEGAL.md](./LEGAL.md)** - Legal disclaimers and acceptable use
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history and updates
- **[Docker Compose Files](./compose/)** - Deployment configurations
- **[Kubernetes Manifests](./k8s/)** - K8s production deployments
- **[CLI Tools](./cli/)** - mosctl command-line utilities
- **[Scripts](./scripts/)** - Validation and setup scripts

- Open an issue for bugs or feature proposals.
- Fork, branch, and submit a PR covered by unit tests and lint checks.
- Sign off commits if your organization requires DCO.

### Contributing

### License

Released under the [Apache License 2.0](LICENSE). See `LEGAL.md` for acceptable use guidance.

---

**Made with ❤️ for MikroTik Network Monitoring**

**Professional DevOps & Monitoring Services:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

## Русский

### 📑 Содержание

- [Зачем этот проект](#зачем-этот-проект)
- [Возможности](#-features--возможности)
- [Быстрый старт за 3 команды](#-quick-start-in-3-commands--быстрый-старт-за-3-команды)
- [Обзор архитектуры](#обзор-архитектуры)
- [Варианты развёртывания](#-deployment-options--варианты-развёртывания)
- [Готовые дашборды](#-pre-configured-dashboards--готовые-дашборды)
- [Конфигурация](#конфигурация)
- [Тесты и проверки](#тесты-и-проверки)
- [Решение проблем](#-troubleshooting--решение-проблем)
- [Безопасность и производительность](#безопасность-и-производительность)
- [Правовое использование](#правовое-использование)
- [Продакшн развёртывание и профессиональная поддержка](#-production-deployment--professional-support)
- [Автор и профессиональные услуги](#-author--professional-services)
- [Поддержка](#-support--поддержка)
- [Документация](#-documentation--документация)
- [Вклад](#вклад)
- [Лицензия](#лицензия-1)

### Зачем этот проект

MikroTik широко используется в малом бизнесе, у интеграторов и в домашних лабораториях, но готового, единообразного стека наблюдаемости почти нет. Здесь собраны проверенные компоненты (Prometheus, Grafana, Loki, Alertmanager и экспортёры), настроенные с учётом особенностей RouterOS, но без привязки к проприетарным решениям.

### Обзор архитектуры

Путь метрик: MikroTik отдаёт данные через API или SNMP → экспортёры → Prometheus → дашборды и алерты Grafana.

Путь логов: MikroTik отправляет syslog → Promtail → Loki → поиск в Grafana.

```
        +-----------------+          +-----------------+
        | MikroTik Router |--API-->  | RouterOS Export |
        | (SNMP / Syslog) |--SNMP->  |   или SNMP Expo |
        |                 |--Syslog->| Promtail        |
        +-----------------+          +-----------------+
                 \                         /
                  \                       /
                 Метрики ------------ Логи
                       \             /
                        \           /
                         v         v
                      Prometheus  Loki
                           \       /
                            \     /
                              Grafana
```

### Конфигурация

`config/mikrotik-devices.yml` хранит список роутеров с обязательными полями `name`, `address`, `exporter`. Поддерживаются типы `routeros` и `snmp`. Можно добавлять произвольные ярлыки для фильтрации в Grafana.

Переменные `.env` управляют учётными данными Grafana, ретенцией Prometheus/Loki и портами сервисов. Для продакшена храните секреты в менеджере секретов и ограничивайте доступы.

### Тесты и проверки

- `scripts/validate-config.sh` – проверка структуры файлов конфигурации.
- `pytest tests/unit` – модульные тесты CLI и валидатора.
- `pytest tests/integration -m compose` – интеграционные смоук-тесты Docker Compose.
- CLI-команды `mosctl` помогают валидировать конфиги и генерировать цели для Prometheus.

### Безопасность и производительность

- Создавайте отдельные read-only учётные записи в RouterOS для SNMP и API.
- Ограничивайте доступы к API/SNMP по адресу, защищайте Grafana и Prometheus обратным прокси.
- Настройте интервалы опроса и ретенцию согласно пропускной способности и диску.
- CI запускает линтеры, анализ зависимостей и сканирование контейнеров (Trivy/Grype) через `scripts/security-scan.sh`.

### Правовое использование

- Следите только за теми сетями и устройствами, на которые у вас есть письменное разрешение.
- MikroTik и RouterOS — торговые марки MikroTik SIA; проект не аффилирован с MikroTik, Grafana Labs или Prometheus.
- Репозиторий не содержит проприетарных файлов MikroTik; все тексты и конфиги созданы с нуля.

### Вклад

- Сообщайте о проблемах через Issues, предлагайте улучшения PR-ами.
- Соблюдайте стиль кода из `scripts/lint.sh`, добавляйте тесты к функциональным изменениям.

### Лицензия

Проект распространяется по [лицензии Apache 2.0](LICENSE). Рекомендации по правомерному использованию описаны в `LEGAL.md`.

---

**Made with ❤️ for MikroTik Network Monitoring**

**Professional DevOps & Monitoring Services:** [run-as-daemon.ru](https://run-as-daemon.ru)
