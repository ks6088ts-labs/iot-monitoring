import asyncio
import logging
from typing import Annotated

import typer
from dotenv import load_dotenv

app = typer.Typer()


def get_log_level(debug: bool) -> int:
    return logging.DEBUG if debug else logging.INFO


def setup_logging(debug: bool = False):
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: " "%(message)s",
        level=get_log_level(debug),
        force=True,
    )


@app.command()
def send_message(
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    from cmds.iothub.send_message import send_message as iothub_send_message

    setup_logging(debug)
    asyncio.run(iothub_send_message())


@app.command()
def receive_direct_method(
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    from cmds.iothub.receive_direct_method import receive_direct_method as iothub_receive_direct_method

    setup_logging(debug)
    asyncio.run(iothub_receive_direct_method())


@app.command()
def upload_to_blob(
    blob_name: Annotated[str, typer.Option(help="Enable debug mode")] = "YourBlobName.jpg",
    path: Annotated[str, typer.Option(help="Path to the image file")] = "image.jpg",
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    from cmds.iothub.upload_to_blob import upload_to_blob as iothub_upload_to_blob

    setup_logging(debug)

    with open(path, "rb") as f:
        image_data = f.read()

    asyncio.run(
        iothub_upload_to_blob(
            blob_name=blob_name,
            image_data=image_data,
        )
    )


@app.command()
def run_prometheus_target(
    num_devices: Annotated[int, typer.Option(help="Number of devices to simulate")] = 3,
    port: Annotated[int, typer.Option(help="Port to run the Prometheus target on")] = 8000,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    from cmds.prometheus.simulator import run_simulators

    setup_logging(debug)
    run_simulators(
        num_devices=num_devices,
        port=port,
    )


@app.command()
def capture_image(
    camera_index: Annotated[int, typer.Option(help="Camera index to capture image from")] = 0,
    path: Annotated[str, typer.Option(help="Path to save the image")] = "image.jpg",
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    from cmds.cv.capture import capture_image as cv_capture_image

    setup_logging(debug)
    data = cv_capture_image(
        camera_index=camera_index,
    )
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    load_dotenv(".env")
    app()
