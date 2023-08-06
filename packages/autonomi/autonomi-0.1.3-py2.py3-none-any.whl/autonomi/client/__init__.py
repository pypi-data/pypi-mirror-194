# Copyright 2022- Autonomi AI, Inc. All rights reserved.
"""Autonomi Cloud Python client

Usage:
    >>> cli = AutonomiClient(api_key, endpoint="https://api.autonomi.ai", verbose=False)
    >>> cli.connect()

"""

from loguru import logger

from autonomi.client._client import BaseClient
from autonomi.client._frameserver import FrameServerClient
from autonomi.client._jobs import JobsClient
from autonomi.client._render import RenderClient
from autonomi.client._search import SearchClient
from autonomi.client._store import StoreClient
from autonomi.client._version import __version__  # fmt: off


class AutonomiClient(BaseClient):
    def __init__(
        self, api_key: str = None, endpoint: str = None, verbose: bool = False
    ):
        super().__init__(api_key=api_key, endpoint=endpoint)
        if verbose:
            logger.enable("autonomi.client._connection")
        else:
            logger.disable("autonomi.client._connection")
            logger.disable("autonomi.client._frameserver")
            logger.disable("autonomi.client._jobs")
            logger.disable("autonomi.client._render")
            logger.disable("autonomi.client._render_utils")
            logger.disable("autonomi.client._search")
            logger.disable("autonomi.client._store")

    def health(self):
        """Get the health of the Autonomi API endpoint"""
        return super().health()

    def status(self):
        """Get the status of the Autonomi API endpoint"""
        return super().status()

    @property
    def frameserver(self):
        """FrameServer API client"""
        return FrameServerClient(
            api_key=self.api_key, endpoint=f"{self.endpoint}/frameserver"
        )

    @property
    def jobs(self):
        """Jobs / Inference API client"""
        return JobsClient(api_key=self.api_key, endpoint=f"{self.endpoint}/jobs")

    @property
    def search(self):
        """Search API client"""
        return SearchClient(api_key=self.api_key, endpoint=f"{self.endpoint}/search")

    @property
    def store(self):
        """Store API client"""
        return StoreClient(api_key=self.api_key, endpoint=f"{self.endpoint}/store")

    @property
    def render(self):
        """Render API client"""
        return RenderClient(api_key=self.api_key, endpoint=self.endpoint)


def connect(api_key: str = None, endpoint: str = None, verbose: bool = False):
    """Connect to the Autonomi API.

    Args:
        api_key (str, optional): API key. Defaults to None and reads from the environment variable.
        endpoint (str, optional): API endpoint. Defaults to None.
        verbose (bool, optional): Enable verbose logging. Defaults to False.

    Returns:
        AutonomiClient: AutonomiClient instance

    Examples:
        >>> cli = AutonomiClient.connect(api_key, endpoint="https://api.autonomi.ai", verbose=False)

        >>> cli.status()
        {'status': 'ok'}

        >>> cli.search.search(...)
    """
    return AutonomiClient(api_key=api_key, endpoint=endpoint, verbose=verbose)
