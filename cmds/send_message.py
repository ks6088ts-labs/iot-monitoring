# https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/async-hub-scenarios/send_message.py
import asyncio
import os
import uuid

from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient


async def send_message_command():
    # The connection string for a device should never be stored in code.
    # For the sake of simplicity we're using an environment variable here.
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    await device_client.connect()

    async def send_test_message(i):
        print("sending message #" + str(i))
        msg = Message("test wind speed " + str(i))
        msg.message_id = uuid.uuid4()
        msg.correlation_id = "correlation-1234"
        msg.custom_properties["tornado-warning"] = "yes"
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        await device_client.send_message(msg)
        print("done sending message #" + str(i))

    # send `3` messages in parallel
    await asyncio.gather(*[send_test_message(i) for i in range(1, 3 + 1)])

    # Finally, shut down the client
    await device_client.shutdown()
