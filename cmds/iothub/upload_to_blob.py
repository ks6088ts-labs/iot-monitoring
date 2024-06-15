# https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/async-hub-scenarios/upload_to_blob.py
import pprint
from logging import getLogger

from azure.core.exceptions import ResourceExistsError
from azure.iot.device.aio import IoTHubDeviceClient
from azure.storage.blob import BlobClient

logger = getLogger(__name__)


async def upload_via_storage_blob(blob_info, image_data: bytes):
    sas_url = "https://{}/{}/{}{}".format(
        blob_info["hostName"],
        blob_info["containerName"],
        blob_info["blobName"],
        blob_info["sasToken"],
    )
    blob_client = BlobClient.from_blob_url(sas_url)
    return blob_client.upload_blob(image_data)


async def upload_to_blob(
    device_client: IoTHubDeviceClient,
    blob_name: str,
    image_data: bytes,
):
    # get the Storage SAS information from IoT Hub.
    storage_info = await device_client.get_storage_info_for_blob(blob_name)
    result = {"status_code": -1, "status_description": "N/A"}

    # Using the Storage Blob V12 API, perform the blob upload.
    try:
        upload_result = await upload_via_storage_blob(storage_info, image_data)
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
