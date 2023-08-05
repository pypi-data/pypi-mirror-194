# Copyright 2022- Autonomi AI, Inc. All rights reserved.
import base64
import io
from typing import List, Union

import numpy as np
import pandas as pd
from PIL import Image

from autonomi.client._client import BaseClient, retry


class SearchClient(BaseClient):
    """Client for the Search API."""

    DEFAULT_TIMEOUT_SEC = 60

    @retry
    def projects(self) -> List[str]:
        """List all projects.

        Returns:
            List[str]: List of project names.
        """
        json_response = self._connection.get(
            route="projects",
            params=dict(public=True),
            timeout=SearchClient.DEFAULT_TIMEOUT_SEC,
        )
        return json_response

    @retry
    def index(
        self,
        project_id: str = "default",
        urls: List[str] = None,
        drop: bool = False,
    ):
        """Index a list of urls / directories of videos.

        Args:
            project_id (str): The project ID. Defaults to "default".
            urls (str): The urls to index.
                None: If urls is None, the entire user-directory will be indexed.

                [<key_prefix>/path, ...]: If urls is a list of dirpaths, then each
                entire sub-directory will be indexed.

                [<key_prefix>/file.mp4, ..]: If urls is a list of files,
                only those files will be indexed.

            drop (bool): Whether to drop the existing index.

        Returns:
            Dict: The job info dictionary.
        """
        data = dict(
            project_id=project_id,
            urls=urls,
            drop=drop,
        )
        json_response = self._connection.post(
            route="index/userdata",
            json=data,
            timeout=SearchClient.DEFAULT_TIMEOUT_SEC,
        )
        return json_response

    @retry
    def reindex(self, project_id: str):
        """Re-index the entire project.

        Args:
            project_id (str): The project ID.
            drop (bool): Whether to drop the existing index.

        Returns:
            Dict: The job info dictionary.
        """
        return self._connection.post(
            route=f"index/project/{project_id}",
            timeout=SearchClient.DEFAULT_TIMEOUT_SEC,
        )

    @retry
    def delete(self, project_id: str):
        """Delete the entire project.

        Args:
            project_id (str): The project ID.

        Returns:
            Dict: The job info dictionary.
        """
        return self._connection.post(
            route=f"delete/{project_id}",
            timeout=SearchClient.DEFAULT_TIMEOUT_SEC,
        )

    @retry
    def search(
        self,
        project_id: str,
        query: str,
        type: str = "scenario",
        topk: int = 30,
        results_per_episode: int = 4,
        metadata: bool = True,
        file_id: str = None,
        features: bool = False,
    ) -> pd.DataFrame:
        """Search for scenarios / objects.

        Args:
            project_id (str): The project ID.
            query (str): The query string.
            type (str, optional): The type of search. Defaults to "scenario".
            topk (int, optional): The number of results to return. Defaults to 30.
            results_per_episode (int, optional): The number of results per episode. Defaults to 4.
            metadata (bool, optional): Whether to include metadata. Defaults to False.
            file_id (str, optional): The file ID. Defaults to None.
            features (bool, optional): Whether to include the feature. Defaults to False.

        Returns:
            pd.DataFrame: The search results.

        """
        if type.lower() not in ("scenario", "object"):
            raise ValueError(f"type must be either 'scenario' or 'object', got {type}")

        json_data = dict(
            project_id=project_id,
            query=query,
            topk=topk,
            results_per_episode=results_per_episode,
            type=type.upper(),
            metadata=metadata,
            file_id=file_id,
            include_feature=features,
        )
        json_response = self._connection.post(
            route="query",
            json=json_data,
            timeout=SearchClient.DEFAULT_TIMEOUT_SEC,
        )
        return pd.DataFrame.from_records(json_response["data"])

    def rsearch(
        self,
        project_id: str,
        image_features: Union[np.ndarray, List[float]] = None,
        image: Image = None,
        image_bytes: str = None,
        type: str = "scenario",
        topk: int = 30,
        results_per_episode: int = 4,
        metadata: bool = True,
        file_id: str = None,
        features: bool = False,
    ) -> pd.DataFrame:
        """Reverse search for a scenario or object instance.

        Args:
            project_id (str): The project ID.
            image_features (Union[np.ndarray, List[float]], optional): The image features.
            image (): PIL Image.
            image_bytes (str, optional): Image encoded in base64.
            type (str, optional): The type of search. Defaults to "scenario".
            topk (int, optional): The number of results to return.
            results_per_episode (int, optional): The number of results per episode.
            metadata (bool, optional): Whether to include metadata.
            file_id (str, optional): The file ID.
            features (bool, optional): Whether to include the feature.

        Returns:
            pd.DataFrame: The search results.

        """
        if type.lower() not in ("scenario", "object"):
            raise ValueError(f"type must be either 'scenario' or 'object', got {type}")

        if image_features:
            if not (
                isinstance(image_features, np.ndarray)
                or isinstance(image_features, list)
            ):
                raise ValueError(
                    "image_features must be a numpy array or a list of floats."
                )
        # Parse image, image_features, or image_bytes
        kwargs = {}
        if image_features:
            if isinstance(image_features, np.ndarray):
                image_features = image_features.tolist()
            kwargs.update({"features": image_features})
        elif image:
            im_bytes_file = io.BytesIO()
            image.save(im_bytes_file, format="PNG")
            im_bytes = im_bytes_file.getvalue()  # im_bytes: image in binary format.
            im_b64 = base64.b64encode(im_bytes)
            kwargs.update({"bytes": im_b64.decode("utf-8")})
        elif image_bytes:
            kwargs.update({"bytes": image_bytes})
        else:
            raise ValueError("Must provide image_features or image or image_bytes.")

        # Make request
        json_data = dict(
            project_id=project_id,
            topk=topk,
            results_per_episode=results_per_episode,
            type=type.upper(),
            metadata=metadata,
            file_id=file_id,
            include_feature=features,
            **kwargs,
        )
        json_response = self._connection.post(
            route="rquery",
            json=json_data,
            timeout=SearchClient.DEFAULT_TIMEOUT_SEC,
        )
        return pd.DataFrame.from_records(json_response["data"])

    @retry
    def stats(self, project_id: str) -> dict:
        """Get the stats of a project."""
        json_response = self._connection.get(
            route=f"stats/{project_id}",
            timeout=SearchClient.DEFAULT_TIMEOUT_SEC,
        )
        return json_response
