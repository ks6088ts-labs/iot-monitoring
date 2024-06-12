# Azure IoT Hub Messaging

## 環境構築

```shell
git clone git@github.com:ks6088ts-labs/azure-ai-services-solutions.git
cd azure-ai-services-solutions/infra

# デプロイ
make deploy
```

- [Azure IoT Hub を使用してデバイスからクラウドにファイルをアップロードする (Python) > IoT Hub への Azure Storage アカウントの関連付け](https://learn.microsoft.com/ja-jp/azure/iot-hub/file-upload-python#associate-an-azure-storage-account-to-iot-hub)
- [IoTHub を経由して Blob Storage にファイルをアップロードするメモ for Python3](https://zenn.dev/tmitsuoka0423/articles/iothub-file-upload-python)

## スクリプト実行 demo

- [Samples for the Azure IoT Hub Device SDK](https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/README.md)

```shell
# 環境変数設定
cp .env.sample .env
```

```shell
# Help
poetry run python main.py --help

# 1. send-message
poetry run python main.py send-message

# 2. receive-direct-method
poetry run python main.py receive-direct-method
# Azure Portal から該当デバイスに対して direct method を送信

# 3. upload-to-blob
poetry run python main.py upload-to-blob --blob-name YYYYMMDD_HHMMSS.jpg

# 4. direct method を受けてカメラ画像を取得してアップロード
# FIXME: 未実装
```

# References

- [Monitoring Azure IoT Hub](https://learn.microsoft.com/en-us/azure/iot-hub/monitor-iot-hub)
