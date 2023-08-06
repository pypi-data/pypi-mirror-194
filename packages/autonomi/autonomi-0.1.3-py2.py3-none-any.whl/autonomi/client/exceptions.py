# Copyright 2022- Autonomi AI, Inc. All rights reserved.


class AutonomiClientException(Exception):
    def __init__(self, status_code, text="AutonomiClientException"):
        self.status_code = status_code
        self.text = text

    def __str__(self):
        return f"""Response Error: [code={self.status_code}, text={self.text}]"""


class MissingAPIKeyException(Exception):
    def __init__(
        self,
        message="""Provide an api_key or set """
        """the AUTONOMI_API_KEY environment variable """
        """before using this client.""",
    ):
        self.message = message


class BadEndpointException(Exception):
    def __init__(self, message="Endpoint unavailable."):
        self.message = message
