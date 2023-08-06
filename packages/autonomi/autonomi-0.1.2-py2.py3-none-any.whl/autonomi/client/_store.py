# Copyright 2022- Autonomi AI, Inc. All rights reserved.
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse

from autonomi.client._client import BaseClient
from autonomi.client.constants import SUPPORTED_VIDEO_FORMATS
from autonomi.client.utils import generate_presigned_url


class StoreClient(BaseClient):
    DEFAULT_TIMEOUT_SEC = 180
    DEFAULT_UPLOAD_TIMEOUT_SEC = 600

    def upload(self, uri: str, schema: Dict[str, str] = None, tags: List[str] = None):
        """Upload a video to the Autonomi Cloud platform.

        Args:
            uri (str): The URI of the video to upload. This can be a local path
                to a video file or a URL to a video file.
        schema (Dict[str, str]): The schema to use for the upload.
                Currently not supported.
        tags (List[str]): Metadata tags to attach to the uploaded file
                for later retrieval.

        Returns:
            dict: The upload response.
        """
        if schema is not None:
            raise NotImplementedError("Schema upload is not yet supported")
        if tags is not None:
            raise NotImplementedError("Tagging is not yet supported")

        scheme = urlparse(uri).scheme
        if scheme in {"http", "https", "s3", "gs"}:
            return self._upload_url(uri)
        elif Path(uri).is_file() and uri.endswith(SUPPORTED_VIDEO_FORMATS):
            return self._upload_file(uri)
        else:
            raise IOError(f"Unsupported URI [uri={uri}]")

    def upload_many(
        self,
        uris: List[str],
        schema: Dict[str, str] = None,
        tags: List[str] = None,
        threads: int = 4,
    ):
        """Upload several videos to the Autonomi Cloud platform.

        Args:
            uris (List[str]): The URIs of the videos to upload. These can be
                local paths to video files or URLs to video files.
            schema (Dict[str, str]): The schema to use for the upload.
            tags (List[str]): Metadata tags to attach to the uploaded file
                for later retrieval.
            threads (int): The number of threads to use for uploading.

        Returns:
            dict: The upload response.
        """
        if schema is not None:
            raise NotImplementedError("Schema upload is not yet supported")
        if tags is not None:
            raise NotImplementedError("Tagging is not yet supported")

        threads = min(threads, len(uris))
        print(f"☁️ Uploading {len(uris)} videos with {threads} threads")
        with ThreadPoolExecutor(threads) as executor:
            responses = executor.map(self.upload, uris, [tags for _ in uris])
            return list(responses)

    def list(
        self,
        regex: str = "*",
        offset: int = 0,
        limit: int = 100,
        tags: List[str] = None,
    ):
        """List all videos in the Autonomi Cloud platform.

        Args:
            regex (str): A regex to filter the list by.
            offset (int): The offset to start the list from.
            limit (int): The maximum number of items to return.
            tags (List[str]): Metadata tags to filter the list by.

        Returns:
            dict: The list response.
        """
        if tags is not None:
            raise NotImplementedError("Tagging is not yet supported")

        response = self._connection.get(
            route="",
            params=dict(regex=regex, offset=offset, limit=limit),
        )
        return response

    def delete(
        self,
        tags: List[str] = None,
    ):
        """Delete all videos in the Autonomi Cloud platform.

        Args:
            regex (str): A regex to filter the list by.
            tags (List[str]): Metadata tags to filter the list by.

        Returns:
            dict: The list response.
        """
        if tags is not None:
            raise NotImplementedError("Tagging is not yet supported")

        return self._connection.post(
            route="delete",
        )

    def _upload_file(self, filename: str):
        """Upload a video to the Autonomi Cloud platform.

        Args:
            filename (str): The path to the video file.

        Returns:
            dict: The upload response.
        """
        # Check if the file is a supported video format
        ext = Path(filename).suffix
        if ext not in SUPPORTED_VIDEO_FORMATS:
            raise IOError("Unsupported video format [ext={ext}, filename={filename}]")

        # Remove the content type header since we're sending a multi-part file
        headers = self._connection.default_headers
        _ = headers.pop("Content-Type")
        with open(filename, "rb") as f:
            response = self._connection.post(
                route="upload/file",
                headers=headers,
                files=dict(file=f),
                raw=True,
                timeout=StoreClient.DEFAULT_UPLOAD_TIMEOUT_SEC,
            )
            if response.status_code == 201:
                print(f"✅ Successfully uploaded [filename={filename}]")
                return response.json()
            else:
                print(
                    f"❌ Failed to upload [filename={filename}, error={response.text}]"
                )
                return None

    def _upload_url(self, url: str):
        """Upload a video URL to the Autonomi Cloud platform.

        Args:
            url (str): The URL to the video.

        Returns:
            dict: The upload response.
        """
        params = {"url": url}
        presigned_url = None
        if urlparse(url).scheme in {"s3", "gs"}:
            try:
                print(f"🔐 Generating pre-signed URL [url={url}]")
                presigned_url = generate_presigned_url(url)
            except Exception as e:
                print(f"❌ Failed to generate pre-signed URL [url={url}, error={e}]")
                return None
            params.update({"presigned_url": presigned_url})
        response = self._connection.post(
            route="upload/url",
            params=params,
            raw=True,
            timeout=StoreClient.DEFAULT_UPLOAD_TIMEOUT_SEC,
        )
        if response.status_code == 201:
            url_str = (
                f"url={url}" + f", presigned_url={presigned_url}"
                if presigned_url
                else ""
            )
            print(f"✅ Uploaded pre-signed URL [{url_str}]")
            return response.json()
        else:
            print(
                f"❌ Failed to upload pre-signed URL [url={url}, error={response.text}]"
            )
            return None
