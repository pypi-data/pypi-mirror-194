# Copyright 2022- Autonomi AI, Inc. All rights reserved.
from dataclasses import dataclass
from typing import Dict

import requests
from loguru import logger
from pydantic import SecretStr

from .exceptions import AutonomiClientException

DEFAULT_API_TIMEOUT_SEC = 30


@dataclass
class Connection:
    api_key: SecretStr
    """API key to connect to the Autonomi API"""

    endpoint: str
    """Endpoint to connect to all the Autonomi API services"""

    def __repr__(self):
        """String representation of the Connection object"""
        return f"[api_key={self.api_key}..., endpoint={self.endpoint}]"

    def _verify(self, route: str) -> bool:
        """Verify that the API key is valid"""
        logger.info(f"{self} :: ")
        return self.api_key is not None

    @property
    def default_headers(self) -> Dict[str, str]:
        """Default headers for all requests"""
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key.get_secret_value()}",
        }

    def _request(
        self,
        route: str,
        json: dict,
        request_func: requests.get,
        headers: dict = None,
        raw: bool = False,
        timeout: int = DEFAULT_API_TIMEOUT_SEC,
        **kwargs,
    ) -> Dict:
        """Make a request to the Autonomi API endpoint.

        Usage:
            >>> from autonomi.client import Connection
            >>> connection = Connection(api_key="...", endpoint="...")
            >>> connection._request(route="...", request_func=requests.post, json={...})

        Args:
            route (str): Route to the endpoint.
            json (dict): JSON payload to send to the endpoint.
            request_func (requests.get): Function to make the request.
            headers (dict, optional): Headers to send with the request.
                Defaults to None.
            raw (bool, optional): Return the raw response. Defaults to False.
            timeout (int, optional): Timeout for the request. Defaults to 30.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Dict: Response from the endpoint
        """
        url = f"{self.endpoint}/{route}"
        logger.info(
            f"request [f={request_func}, url={url}, json={json}, headers={headers}, kwargs={kwargs}]"
        )
        try:
            # Make the request
            headers = self.default_headers if headers is None else headers
            response = request_func(
                url, json=json, headers=headers, timeout=timeout, **kwargs
            )

            # Raise an exception if the request failed
            response.raise_for_status()

            # Log the response
            logger.debug(
                f"""request successful [url={url}, json={json}, headers={headers}, kwargs={kwargs}"""
                f"""response.status_code={response.status_code}, """
                f"""response.text={response.text}]"""
            )

            # Return the raw response if requested
            if raw:
                return response

            # Otherwise, return the JSON response
            return response.json()
        except Exception as e:
            logger.error(
                f"request failed [url={url}, json={json}, headers={headers}, e={e}]"
            )
            raise AutonomiClientException(
                status_code=response.status_code, text=response.text
            )

    def post(
        self,
        route: str,
        json: dict = None,
        headers: dict = None,
        raw: bool = False,
        timeout: int = DEFAULT_API_TIMEOUT_SEC,
        **kwargs,
    ) -> Dict:
        """Make a POST request to the Autonomi API endpoint.

        Usage:
            >>> from autonomi.client import Connection
            >>> connection = Connection(api_key="...", endpoint="...")
            >>> connection.post(route="...", json={...})

        Args:
            route (str): Route to the endpoint.
            json (dict): JSON payload to send to the endpoint.
            headers (dict, optional): Headers to send with the request.
                Defaults to None.
            raw (bool, optional): Return the raw response. Defaults to False.
            timeout (int, optional): Timeout for the request. Defaults to 30.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Dict: Response from the endpoint
        """
        return self._request(
            route,
            json,
            request_func=requests.post,
            headers=headers,
            raw=raw,
            timeout=timeout,
            **kwargs,
        )

    def get(
        self,
        route: str,
        json: dict = None,
        headers: dict = None,
        raw: bool = False,
        timeout: int = DEFAULT_API_TIMEOUT_SEC,
        **kwargs,
    ) -> Dict:
        """Make a GET request to the Autonomi API endpoint.

        Usage:
            >>> from autonomi.client import Connection
            >>> connection = Connection(api_key="...", endpoint="...")
            >>> connection.get(route="...")

        Args:
            route (str): Route to the endpoint.
            json (dict): JSON payload to send to the endpoint.
            headers (dict, optional): Headers to send with the request.
                Defaults to None.
            raw (bool, optional): Return the raw response. Defaults to False.
            timeout (int, optional): Timeout for the request. Defaults to 30.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Dict: Response from the endpoint
        """
        return self._request(
            route,
            json,
            request_func=requests.get,
            headers=headers,
            raw=raw,
            timeout=timeout,
            **kwargs,
        )
