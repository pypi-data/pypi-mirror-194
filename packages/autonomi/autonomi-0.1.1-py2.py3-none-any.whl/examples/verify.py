# Copyright 2022- Autonomi AI, Inc. All rights reserved.
import os

from autonomi.client import AutonomiClient

print("Attempting to read API key from environment variable AUTONOMI_API_KEY")

AUTONOMI_API_KEY = os.environ.get("AUTONOMI_API_KEY", None)
if AUTONOMI_API_KEY is None:
    raise ValueError(
        "Missing API key. Please set the environment variable AUTONOMI_API_KEY"
    )

# Initialize the client
cli = AutonomiClient(api_key=AUTONOMI_API_KEY)
print(cli)
