[![test](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/test.yaml?query=branch%3Amain)
[![docker](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/docker.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/docker.yaml?query=branch%3Amain)

# iot-monitoring

## シナリオ

### [1_grafana-prometheus](./docs/1_grafana-prometheus/README.md)

Prometheus でメトリクスを収集し、Grafana で可視化する IoT デバイスの監視サービス

[![architecture](./docs/1_grafana-prometheus/architecture.png)](./docs/1_grafana-prometheus/architecture.png)

### [2_iot-hub-messaging](./docs/2_iot-hub-messaging/README.md)

Azure IoT Hub でデバイスからクラウドにファイルをアップロードする IoT デバイスの監視サービス

[![architecture](./docs/2_iot-hub-messaging/architecture.png)](./docs/2_iot-hub-messaging/architecture.png)
