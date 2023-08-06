# Copyright 2022- Autonomi AI, Inc. All rights reserved.
import base64
from urllib.request import urlopen

import cv2
import numpy as np
import pandas as pd
from IPython.core.display import HTML, display
from loguru import logger

from autonomi.client._client import BaseClient
from autonomi.client._frameserver import FrameServerClient
from autonomi.client._render_utils import (
    gallery,
    jupyter_notebook_b64_formatters,
    render_image_with_bboxes,
)
from autonomi.client.constants import DeepTagMetadata, StoreMetadata
from autonomi.client.utils import apply_parallel

MAX_STORE_FILES = 100_000


class RenderClient(BaseClient):
    """Client for the Render API."""

    def __init__(self, api_key: str = None, endpoint: str = None):
        super().__init__(api_key=api_key, endpoint=endpoint)
        self._frameserver_client = FrameServerClient(
            api_key=self.api_key, endpoint=f"{self.endpoint}/frameserver"
        )
        self._store_client = FrameServerClient(
            api_key=self.api_key, endpoint=f"{self.endpoint}/store"
        )

    def _metadata_join(self, df: pd.DataFrame, limit: int = MAX_STORE_FILES):
        """Join the results results dataframe with the store metadata.

        This is to fetch the "file_id" for the search results, which
        in result is used by the frameserver to fetch and render
        individual frames.
        """
        store_df = self._store_client.list(limit=limit)
        logger.debug(f"store len(items)={len(store_df)}")
        # Join search results with store metadata
        return df.join(
            store_df.set_index(StoreMetadata.FILE_ID),
            on=StoreMetadata.FILE_ID,
        )

    def preview(
        self,
        results_df: pd.DataFrame,
        width: int = 300,
        preview: str = "img",
        crop: bool = False,
        render: str = "gallery",
        threads: int = 0,
    ) -> str:
        """Render the dataframe inline.

        Args:
            results_df (pd.DataFrame): Results dataframe.
            width (int, optional): Width of the rendered image. Defaults to 300.
            preview (str, optional): Preview type. Defaults to "img".
                Options include ["img", "img_url"].
            crop (bool, optional): Crop the image to the bounding box. Defaults to False.
            render (str, optional): Render the results in a specific format.
                Options include: [None, "datatable", "gallery"].
                Rendering as None returns the dataframe. Defaults to "gallery".
            threads (int, optional): Number of threads to use for rendering. Defaults to 0.

        Returns:
            str: Rendered HTML string.
        """
        if preview not in (
            "img_url",
            "img",
        ):
            raise ValueError(f"Unknown preview={preview} type")

        if render not in (
            None,
            "datatable",
            "gallery",
        ):
            raise ValueError(f"Unknown render={render} type")

        # Join the results results dataframe with the store
        # if StoreMetadata.FILE_ID not in results_df.columns
        if StoreMetadata.FILE_ID not in results_df.columns:
            results_df = self._metadata_join(results_df)

        assert StoreMetadata.FILE_ID in results_df.columns
        assert StoreMetadata.FRAME_ID in results_df.columns
        df = results_df.copy()

        # Implement various preview functions (img/video)
        def img_url_preview(row):
            """Preview row by fetching the image url."""
            try:
                json = self._frameserver_client.get_video_frame(
                    row[StoreMetadata.FILE_ID],
                    int(row[StoreMetadata.FRAME_ID]),
                )
            except Exception as e:
                logger.warning(f"Failed to fetch frame: {e}")
                return ""
            return json["presigned_url"]

        def frame_preview(row):
            """Preview row by rendering base64 encoded image inline.
            row
            -> (file_id, frame_id)
            -> fetch image url
            -> overlay bboxes
            -> encode and convert to base64
            """
            try:
                json = self._frameserver_client.get_video_frame(
                    row[StoreMetadata.FILE_ID],
                    int(row[StoreMetadata.FRAME_ID]),
                )
            except Exception as e:
                logger.warning(f"Failed to fetch frame: {e}")
                return b""

            # Fetch URL and render bboxes / crops
            url = json["presigned_url"]
            with urlopen(url) as f:
                im_arr = np.array(bytearray(f.read()), dtype=np.uint8)
            img = cv2.imdecode(im_arr, -1)

            # Render with bbox support
            boxes = (
                np.float32(row[DeepTagMetadata.BOXES])
                if DeepTagMetadata.BOXES in row
                else None
            )
            labels = (
                row[DeepTagMetadata.LABELS] if DeepTagMetadata.LABELS in row else None
            )
            vis = render_image_with_bboxes(img, boxes=boxes, labels=labels, crop=crop)

            # Encode jpeg and convert to base64
            _, im_buf = cv2.imencode(".jpg", vis)
            return base64.b64encode(im_buf)

        # Preview function to call on a per-row basis
        preview_func = {
            "img_url": img_url_preview,
            "img": frame_preview,
        }[preview]

        # Render asynchronously
        preview_df = apply_parallel(df, preview_func, threads=threads)
        # Insert the preview column as the first column
        df.insert(0, preview, preview_df)

        # Return dataframe if render is None
        if render is None:
            return df

        # Fetch URLs and render media objects in-line
        _formatters = jupyter_notebook_b64_formatters(width=width)
        formatters = {
            "img": _formatters["img"],
        }

        # Return fully rendered inlined objects as dataframe
        if render == "datatable":
            html = HTML(df.to_html(escape=False, formatters=formatters))
        elif render == "gallery":
            html = gallery(
                df[preview].values,
                formatter=formatters[preview],
            )
        else:
            raise ValueError(f"Unknown render={render} type")

        # Render in notebook
        display(html)
