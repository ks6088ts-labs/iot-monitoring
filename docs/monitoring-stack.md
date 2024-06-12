# monitoring-stack

## 事前条件

- [Docker](https://www.docker.com/products/docker-desktop/)

## シナリオ

### Docker Compose で監視サービスを構築する

監視サービスを構築し、ノードのメトリクスを収集・可視化します。
以下のコマンドでローカル環境に監視サービスを構築します。

```shell
# ログを標準出力に表示するため -d オプションを付けません
docker compose up

# Access to Grafana at http://localhost:3000
# Type username and password as "admin"
# Set your new password
# Open dashboard "Node Exporter Full"
```

http://localhost:3000 にアクセスし、Grafana にログインします。  
初回ログイン時のユーザ名とパスワードはどちらも `admin` です。  
パスワードを変更する画面が表示されるので、新しいパスワードを設定します。  
Dashboards > Services > Node Exporter Full を開くと、ノードのメトリクスが表示されます。  
表示する time range を短くしたり、自動更新間隔を短くすると変化が見やすくなります。

### ノードのメトリクスを変化させてみる

以下のコマンドで CPU 使用率を上げ、メトリクスの変化を確認します。

```shell
# ノードエクスポーターのコンテナにログインします
docker compose exec node-exporter sh

# メトリクスを変化させるために CPU を使用します
# 以下では負荷をかけるために 3 つのプロセスを起動します)
yes > /dev/null &
yes > /dev/null &
yes > /dev/null &

# PID を確認して kill して後片付けをします
ps
kill <PID0> <PID1> <PID2>
```

### Alertmanager でアラートを設定する

Alertmanager は [CONFIGURATION](https://prometheus.io/docs/alerting/latest/configuration/) を編集し、アラートを設定します。

#### Slack にアラートを通知するための設定

[Sending messages using incoming webhooks](https://api.slack.com/messaging/webhooks) を参考に、Webhook URL を払い出します。
払い出した URL は、[alertmanager.yml](./configs/alertmanager/alertmanager.yml) の `slack_api_url` に設定します。

#### アラート通知を確認する

アラートのルール設定は [alert_rules.yml](./configs/prometheus/alert_rules.yml) で定義されており、以下のルールが設定されています。

- InstanceDown: 一定時間以上メトリクスが収集されない場合
- APIHighRequestLatency: API のレイテンシが一定時間以上閾値を超えた場合

ここでは InstanceDown のアラートを発生させるため、以下のコマンドで Node Exporter を停止します。

```shell
docker compose stop node-exporter
```

一定時間後に Slack にアラート通知が届くことを確認します。

### Prometheus

- [What is Prometheus?](https://prometheus.io/docs/introduction/overview/)
- [ALERTING RULES](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/#alerting-rules)

### Grafana

- [Grafana > Data sources > Prometheus](https://grafana.com/docs/grafana/latest/datasources/prometheus/)
- [Grafana で Dashboard と DataSource の設定をファイルで管理する[Configuration as Code]](https://zenn.dev/ring_belle/articles/grafana-cac-docker)
- [Prometheus + Node_exporter + Grafana でシステム管理](https://qiita.com/Charon9/items/09745a2ca1279045f10f)
- [All dashboards > Node Exporter Full](https://grafana.com/grafana/dashboards/1860-node-exporter-full/)
- [node-exporter-full.json](https://raw.githubusercontent.com/rfmoz/grafana-dashboards/master/prometheus/node-exporter-full.json)
