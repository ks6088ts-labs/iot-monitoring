import asyncio
import logging
from typing import Annotated

import typer
from dotenv import load_dotenv

from cmds.iothub.receive_direct_method import receive_direct_method as iothub_receive_direct_method
from cmds.iothub.send_message import send_message as iothub_send_message
from cmds.iothub.upload_to_blob import upload_to_blob as iothub_upload_to_blob

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
    setup_logging(debug)
    asyncio.run(iothub_send_message())


@app.command()
def receive_direct_method(
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)
    asyncio.run(iothub_receive_direct_method())


@app.command()
def upload_to_blob(
    blob_name: Annotated[str, typer.Option(help="Enable debug mode")] = "YourBlobName",
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)
    asyncio.run(iothub_upload_to_blob(blob_name=blob_name))


if __name__ == "__main__":
    load_dotenv(".env")
    app()
