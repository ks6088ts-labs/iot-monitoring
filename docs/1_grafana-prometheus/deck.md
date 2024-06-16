---
marp: true
---

# IoT Monitoring サービスの構築を通したハンズオン

1. Docker Compose で監視サービスを構築する
2. Azure IoT Hub を利用したデバイスとクラウドの双方向通信

---

# 1. Docker Compose で監視サービスを構築する

**アーキテクチャ図**

- Grafana
- Prometheus
- Node exporter
- Alertmanager

---

# 実験

## 1-1. ノードのメトリクスを変化させてみる

Node Exporter のコンテナに入って CPU 利用率を上げてメトリクスの変化を確認します。

## 1-2. Slack にアラートを発報させてみる

1. Alertmanager の設定に Slack の Incoming Webhook URL を入れる
1. Node Exporter コンテナを停止させて数分待つ
1. Slack に通知が来るか確認

---

# 2. Azure IoT Hub を利用したデバイスとクラウドの双方向通信

**アーキテクチャ図**

- Azure AI Services
- Azure IoT Hub
- Azure Blob Storage
- Azure Cosmos DB
- Device
  - Raspberry Pi
  - Simulator

---

# 2. Azure IoT Hub を利用したデバイスとクラウドの双方向通信

**IoT 固有の要素**

- MQTT: 軽量, 双方向通信
- プロビジョニング: JIT

---

# 実験

## 2-1. Device -> Cloud へのメッセージ送信

デバイスからスクリプト実行して Cosmos DB にデータが投入される

## 2-2. Device <- Cloud へのコマンド送信

遠隔からデバイスに対してコマンドを発行

## 2-3. ファイルをアップロード

デバイスが IoT Hub から接続情報を取得し、Blob Storage にファイルアップロード

## 2-4. Device <- Cloud へのコマンドを受けて画像をアップロード

遠隔から現場のデータをオンデマンドで吸い上げる
