# https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/async-hub-scenarios/receive_direct_method.py
import asyncio
import json
import os
import time

from azure.iot.device import MethodResponse
from azure.iot.device.aio import IoTHubDeviceClient

from cmds.cv.capture import capture_image
from cmds.iothub.upload_to_blob import upload_to_blob


async def receive_direct_method():
    # The connection string for a device should never be stored in code.
    # For the sake of simplicity we're using an environment variable here.
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    await device_client.connect()

    # Define behavior for handling methods
    async def method_request_handler(method_request):
        # Determine how to respond to the method request based on the method name
        if method_request.name == "method1":
            print(method_request.payload)
            print(f"{type(method_request.payload)}")
            payload = {"result": True, "data": "some data"}  # set response payload
            status = 200  # set return status code
            print("executed method1")
        elif method_request.name == "method2":
            payload = {"result": True, "data": 1234}  # set response payload
            status = 200  # set return status code
            print("executed method2")
        elif method_request.name == "capture_photo":
            try:
                payload_dict = method_request.payload
                # if method_request.payload is str then use json.loads to convert it to dict
                if isinstance(method_request.payload, str):
                    payload_dict = json.loads(method_request.payload)
                camera_index = payload_dict.get("camera_index", 0)
                blob_name = payload_dict.get("blob_name", time.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg")

                debug = False
                if debug:
                    # read image from file for debugging purposes
                    with open("./artifacts/image.jpg", "rb") as f:
                        image_data = f.read()
                else:
                    # capture image from camera
                    image_data = capture_image(camera_index=camera_index)

                await upload_to_blob(
                    device_client=device_client,
                    blob_name=blob_name,
                    image_data=image_data,
                )
                payload = {"result": True, "data": 1234}  # set response payload
                status = 200  # set return status code
                print("executed capture_photo")
            except Exception as e:
                payload = {"result": False, "data": str(e)}
                status = 500
        else:
            payload = {"result": False, "data": "unknown method"}  # set response payload
            status = 400  # set return status code
            print("executed unknown method: " + method_request.name)

        # Send the response
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        await device_client.send_method_response(method_response)

    # Set the method request handler on the client
    device_client.on_method_request_received = method_request_handler

    # Define behavior for halting the application
    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                print("Quitting...")
                break

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for method calls
    await user_finished

    # Finally, shut down the client
    await device_client.shutdown()
