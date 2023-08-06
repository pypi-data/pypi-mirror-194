# Copyright 2022- Autonomi AI, Inc. All rights reserved.
import os

import typer
from click import ClickException
from rich.console import Console

from autonomi.client import AutonomiClient

console = Console()
app_cli = typer.Typer(name="app", help="Autonomi Cloud CLI.", no_args_is_help=True)
store_cli = typer.Typer(
    name="store", help="Autonomi Cloud Store CLI.", no_args_is_help=True
)


def api_key_from_env_or_raise():
    """Read API key from environment variable AUTONOMI_API_KEY. or raise ValueError"""
    AUTONOMI_API_KEY = os.environ.get("AUTONOMI_API_KEY", None)
    if AUTONOMI_API_KEY is None:
        raise ValueError(
            "Missing API key. Please set the environment variable AUTONOMI_API_KEY"
        )
    return AUTONOMI_API_KEY


def aws_creds_from_env():
    """Read AWS credentials from environment variables."""
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
    # AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", None)
    AWS_PROFILE = os.environ.get("AWS_PROFILE", None)
    return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_PROFILE  # , AWS_DEFAULT_REGION


def gcp_creds_from_env():
    """Read GCP credentials from environment variables."""
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", None
    )
    return GOOGLE_APPLICATION_CREDENTIALS


def check_cloud_creds_from_env_or_raise():
    """Read cloud credentials from environment variables or raise ValueError"""
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_PROFILE = aws_creds_from_env()
    if AWS_ACCESS_KEY_ID is not None and AWS_SECRET_ACCESS_KEY is not None:
        return True

    if AWS_PROFILE is not None:
        return True

    GOOGLE_APPLICATION_CREDENTIALS = gcp_creds_from_env()
    if GOOGLE_APPLICATION_CREDENTIALS is not None:
        return True

    raise ValueError(
        """Missing cloud credentials. """
        """Please set the environment variables.\n"""
        """\t1. AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY OR\n"""
        """\t2. AWS_PROFILE OR\n"""
        """\t3. GOOGLE_APPLICATION_CREDENTIALS"""
    )


@app_cli.command("verify", help="Verify API key.")
def verify():
    api_key = api_key_from_env_or_raise()
    cli = AutonomiClient(api_key=api_key)
    print(cli)


@store_cli.command(
    "upload",
    help="Upload directory (e.g. /path/to/videos/ or s3://<bucket>/<directory>, or gs://<bucket>/<directory>).",
)
def store_upload(directory: str = typer.Option(..., "-d", "--directory")):
    from itertools import chain
    from pathlib import Path
    from urllib.parse import urlparse

    from cloudpathlib import CloudPath

    from autonomi.client.constants import SUPPORTED_VIDEO_FORMATS

    # Check the API key
    api_key = api_key_from_env_or_raise()

    # Initialize the client
    cli = AutonomiClient(api_key=api_key)
    print(cli)

    # Check the remote directory scheme
    scheme = urlparse(directory).scheme
    if scheme in {"s3", "gs"}:
        # Check the cloud credentials for generating pre-signed URLs
        check_cloud_creds_from_env_or_raise()

        # Upload video files in the remote directory
        path = CloudPath(directory)
        if not path.exists():
            raise ValueError(f"Remote path {directory} does not exist.")
    else:
        # Upload local video files
        path = Path(directory)

    # Find all video files in the directory
    paths = list(
        chain.from_iterable(path.rglob(f"*{ext}") for ext in SUPPORTED_VIDEO_FORMATS)
    )
    console.print(
        f"[bold white]Found videos={len(list(paths))} (path={directory})[/bold white]"
    )

    # Upload the video files
    response = cli.store.upload_many([str(path) for path in paths])
    if response:
        console.print(
            f"🥇 [bold white]Succesfully uploaded videos (videos={len(response)}, path={directory})[/bold white]"
        )
    else:
        raise ClickException(f"❌ Failed to upload videos (path={directory})")

    # Re-index the uploaded videos
    response = cli.frameserver.index()
    if response:
        console.print("💽 [bold white]Re-indexing videos.[/bold white]")
    else:
        raise ClickException("❌ Failed to re-index videos.")


@store_cli.command("list", help="List user uploaded files.")
def store_list(limit: int = 100):
    from autonomi.client.utils import as_dataframe

    cli = AutonomiClient(api_key=api_key_from_env_or_raise())
    response = cli.store.list(limit=limit)
    if response is not None:
        if len(response) == 0:
            console.print("[grey]No files found.[/grey]")
        else:
            console.print(as_dataframe(response))
    else:
        raise ClickException("❌ Failed to list files.")


app_cli.add_typer(store_cli)


if __name__ == "__main__":
    app_cli()
