# https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/async-hub-scenarios/upload_to_blob.py
import os
import pprint
from logging import getLogger

from azure.core.exceptions import ResourceExistsError
from azure.iot.device.aio import IoTHubDeviceClient
from azure.storage.blob import BlobClient

logger = getLogger(__name__)


async def upload_via_storage_blob(blob_info):
    print("Azure Blob storage v12 - Python quickstart sample")
    sas_url = "https://{}/{}/{}{}".format(
        blob_info["hostName"],
        blob_info["containerName"],
        blob_info["blobName"],
        blob_info["sasToken"],
    )
    blob_client = BlobClient.from_blob_url(sas_url)

    # The following file code can be replaced with simply a sample file in a directory.

    # Create a file in local Documents directory to upload and download
    local_file_name = "artifacts/data.jpg"
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), local_file_name)

    # Write text to the file
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    # Create a file in local Documents directory to upload and download
    # file = open(filename, "w")
    # file.write("Hello, World!")
    # file.close()

    # Perform the actual upload for the data.
    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
    # # Upload the created file
    with open(filename, "rb") as data:
        # filename should be YYYYMMDDHHMMSS.jpg
        result = blob_client.upload_blob(data)

    return result


async def upload_to_blob(blob_name: str):
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    await device_client.connect()

    # get the Storage SAS information from IoT Hub.
    storage_info = await device_client.get_storage_info_for_blob(blob_name)
    result = {"status_code": -1, "status_description": "N/A"}

    # Using the Storage Blob V12 API, perform the blob upload.
    try:
        upload_result = await upload_via_storage_blob(storage_info)
        if hasattr(upload_result, "error_code"):
            result = {
                "status_code": upload_result.error_code,
                "status_description": "Storage Blob Upload Error",
            }
        else:
            result = {"status_code": 200, "status_description": ""}
    except ResourceExistsError as ex:
        if ex.status_code:
            result = {"status_code": ex.status_code, "status_description": ex.reason}
        else:
            print("Failed with Exception: {}", ex)
            result = {"status_code": 400, "status_description": ex.message}

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)

    if result["status_code"] == 200:
        await device_client.notify_blob_upload_status(
            storage_info["correlationId"], True, result["status_code"], result["status_description"]
        )
    else:
        await device_client.notify_blob_upload_status(
            storage_info["correlationId"],
            False,
            result["status_code"],
            result["status_description"],
        )

    # Finally, shut down the client
    await device_client.shutdown()
