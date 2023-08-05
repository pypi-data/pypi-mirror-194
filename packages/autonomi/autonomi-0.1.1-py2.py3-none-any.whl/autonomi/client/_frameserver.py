# Copyright 2022- Autonomi AI, Inc. All rights reserved.
from typing import Dict

from autonomi.client._client import BaseClient, retry


class FrameServerClient(BaseClient):
    """Client for the FrameServer API."""

    DEFAULT_TIMEOUT_SEC = 30

    @retry
    def index(self):
        """Re-index user-files."""
        return self._connection.post(
            route="index",
            timeout=FrameServerClient.DEFAULT_TIMEOUT_SEC,
        )

    @retry
    def presign_url(self, url: str) -> str:
        """Get a presigned URL for a video file

        Args:
            url (str): URL to the video file.

        Returns:
            str: Presigned URL for the video file.
        """

        print(f"Presigning URL: {url}")
        response = self._connection.post(
            route="presign_url",
            json=dict(url=url),
        )
        return response["presigned_url"]

    @retry
    def get_video(self, video_id: str) -> Dict:
        """Get a video.

        Args:
            video_id (str): ID of the video to get the frame from

        Returns:
            Dict: Frame data as JSON response
        """
        json_response = self._connection.get(
            route=f"video/{video_id}",
            timeout=self.DEFAULT_TIMEOUT_SEC,
        )
        return json_response

    @retry
    def get_video_frame(self, video_id: str, frame_id: int) -> Dict:
        """Get a frame from a video.

        Args:
            video_id (str): ID of the video to get the frame from
            frame_id (int): ID of the frame to get

        Returns:
            Dict: Frame data as JSON response
        """
        json_response = self._connection.get(
            route=f"frame/{video_id}/{frame_id}",
            timeout=self.DEFAULT_TIMEOUT_SEC,
        )
        return json_response

    @retry
    def get_video_segment(
        self,
        video_id: str,
        frame_id: int,
        window: int = 100,
        skip: int = 4,
        width: int = 400,
        fps: int = 10,
        extension: str = "mp4",
    ) -> Dict:
        """Get a segment from a video.

        Args:
            video_id (str): ID of the video to get the snippet from
            frame_id (int): ID of the frame to get
            window (int, optional): Number of frames to include in the snippet.
                Defaults to 100.
            skip (int, optional): Number of frames to skip between each frame in the snippet.
            width (int, optional): Width of the snippet. Defaults to 400.
            fps (int, optional): Frames per second of the snippet. Defaults to 10.
            extension (str, optional): Extension of the snippet. Defaults to "mp4".

        Returns:
            Dict: Snippet data as JSON response
        """
        json_response = self._connection.get(
            route=f"video/{video_id}/{frame_id}",
            params=dict(
                window=window,
                skip=skip,
                width=width,
                fps=fps,
                extension=extension,
            ),
            timeout=self.DEFAULT_TIMEOUT_SEC,
        )
        return json_response
