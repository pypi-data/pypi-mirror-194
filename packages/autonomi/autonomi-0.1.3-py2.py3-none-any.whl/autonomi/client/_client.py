# Copyright 2022- Autonomi AI, Inc. All rights reserved.
import os

import sentry_sdk
import tenacity
from loguru import logger
from pydantic import SecretStr

from autonomi.client._connection import Connection
from autonomi.client._version import __version__
from autonomi.client.constants import (
    AUTONOMI_API_ENDPOINT,
    AUTONOMI_TELEMETRY,
    SENTRY_DSN,
)
from autonomi.client.exceptions import MissingAPIKeyException

retry = tenacity.retry(
    stop=tenacity.stop.stop_after_attempt(1) | tenacity.stop.stop_after_delay(10),
    reraise=True,
)

if AUTONOMI_TELEMETRY:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        debug="SENTRY_DEBUG" in os.environ,
        traces_sample_rate=1.0,
        release=__version__,
    )
else:
    logger.info("Autonomi client telemetry is disabled.")


class BaseClient:
    DEFAULT_TIMEOUT_SEC = 30

    def __init__(self, api_key: str = None, endpoint: str = None):
        """Initialize the client

        Args:
            api_key (str, optional): API key. Defaults to None.
            endpoint (str, optional): API endpoint. Defaults to None.
                For example, https://api.autonomi.ai/v1
                For local development, http://localhost:8000/v1

        Raises:
            MissingAPIKeyException: If no API key is provided
        """
        if endpoint is None:
            endpoint = AUTONOMI_API_ENDPOINT
        self.endpoint = endpoint
        # TODO: Check endpoint status

        if api_key is None or api_key == "":
            api_key = os.environ.get("AUTONOMI_API_KEY", None)
        if api_key is None:
            raise MissingAPIKeyException()

        # Establish connection with API key authentication
        self.api_key = api_key
        self._connection = Connection(
            api_key=SecretStr(self.api_key), endpoint=self.endpoint
        )

    def __repr__(self):
        """Return a string representation of the client"""
        return (
            f"""{self.__class__.__name__} [v{__version__}] :: """
            f"""[{self.endpoint}, """
            f"""api_key={self.api_key[:4]}***, """
            f"""health={self.__health__repr__()}, """
            f"""auth={self.__verify_repr__()}]"""
        )

    def __health__repr__(self):
        """Return a string representation of the health of the client"""
        try:
            healthcheck = self.health()["status"].lower() == "ok"
            if healthcheck:
                health = "\033[92mOK\033[0m"
            else:
                health = "\033[91mUNAVAILABLE\033[0m"
        except Exception:
            health = "\033[91mUNAVAILABLE\033[0m"
        return health

    def __verify_repr__(self):
        """Return a string representation of user authentication"""
        if self.verify():
            return "\033[92mOK\033[0m"
        else:
            return "\033[91mFAILED\033[0m"

    def verify(self):
        """Verify the client is connected to the Autonomi API endpoint"""
        try:
            return self.status()["status"].lower() == "ok"
        except Exception:
            return False

    @retry
    def health(self):
        """Get the health of the Autonomi API endpoint"""
        return self._connection.get(route="health")

    @retry
    def status(self):
        """Get the status of the Autonomi API endpoint"""
        return self._connection.get(route="status")
