# Copyright 2022- Autonomi AI, Inc. All rights reserved.
import os

SUPPORTED_VIDEO_FORMATS = (".mp4", ".avi", ".mov")

AUTONOMI_API_URL = "api.autonomi.ai"
AUTONOMI_API_ENDPOINT = os.getenv(
    "AUTONOMI_API_ENDPOINT", f"https://{AUTONOMI_API_URL}/v1"
)

AUTONOMI_TELEMETRY = bool(os.getenv("AUTONOMI_TELEMETRY", True))
SENTRY_DSN = os.getenv(
    "SENTRY_DSN",
    "https://b170c53440054d318d3987c1eaa7bd6a@o4504121578487808.ingest.sentry.io/4504730414678016",
)


class StoreMetadata:
    """Column names for the store dataframe."""

    FILE_URL = "file_url"
    """Remote file URL."""
    FILE_ID = "file_id"
    """Unique file identifier."""
    FRAME_ID = "frame_id"
    """Unique video frame identifier."""


class SearchMetadata:
    SCORES = "search_scores"
    """Search relevance score."""
    FEATURES = "search_features"
    """Extracted instance features."""


class DeepTagMetadata:
    """Column names for the deeptag dataframe."""

    LABELS = "pred_labels"
    """Predicted class label."""
    SCORES = "pred_scores"
    """Predicted class score. """
    BOXES = "pred_boxes"
    """Predicted bounding box coords in [0, 1]."""
    BOX_ID = "box_id"
    """Unique bounding box identifier."""
