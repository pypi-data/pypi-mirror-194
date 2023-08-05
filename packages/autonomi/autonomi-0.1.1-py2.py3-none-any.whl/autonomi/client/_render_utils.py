# Copyright 2022- Autonomi AI, Inc. All rights reserved.
import base64
from typing import Callable, List, Optional

import cv2
import numpy as np
import requests
from IPython.core.display import HTML, Image
from loguru import logger


def jupyter_notebook_url_formatters(width: int = 300) -> dict:
    """Get formatters for displaying images and videos in Jupyter Notebook."""
    formatters = {
        "img": lambda x: '<img src="data:image/png;base64,%s" width="%d" />'
        % (Image(data=x, format="jpg")._data_and_metadata(), width),
        "gif": lambda x: '<img src="data:image/gif;base64,%s" width="%d" />'
        % (Image(data=x, format="gif")._data_and_metadata(), width),
        "mp4": lambda x: f'<video autoplay loop width={width}><source src="data:video/mp4;base64,%s" type="video/mp4"></video>'
        % (base64.b64encode(requests.get(x).content).decode()),
    }
    return formatters


def jupyter_notebook_b64_formatters(width: int = 300) -> dict:
    """Get base64 formatters for displaying images and videos in Jupyter Notebook."""
    formatters = {
        "img": lambda x: '<img src="data:image/png;base64,%s" width="%d" />'
        % (x.decode(), width),
        "gif": lambda x: '<img src="data:image/gif;base64,%s" width="%d" />'
        % (x.decode(), width),
        "mp4": lambda x: f'<video autoplay loop width={width}><source src="data:video/mp4;base64,%s" type="video/mp4"></video>'
        % (x.decode()),
    }
    return formatters


def render_image_with_bboxes(
    img: np.ndarray,
    boxes: np.ndarray = None,
    labels: List[str] = None,
    crop: bool = False,
    thickness: int = 4,
) -> np.ndarray:
    """Render image with bounding boxes.

    Args:
        img (np.ndarray): Image to render.
        boxes (np.ndarray): Bounding boxes to render.
        labels (List[str]): Labels for the bounding boxes.
        crop (bool): Crop the image to the bounding box.
        thickness (int): Thickness of the bounding box.

    Returns:
        np.ndarray: Rendered image.
    """
    logger.debug(
        f"Rendering image [img={img.shape[:2]}, boxes={len(boxes) if boxes is not None else None}]."
    )
    H, W, _ = img.shape
    if boxes is None:
        logger.debug("No boxes to render, exiting early")
        return img

    # Render normalized bboxes coordinates
    boxes = boxes.copy()
    if labels is None:
        labels = [""] * len(boxes)
    ndim = boxes.ndim
    boxes[..., 0::2] *= W
    boxes[..., 1::2] *= H
    boxes = boxes.astype(int)
    if (boxes[..., ::2].max() > W).any() or (boxes[..., 1::2] > H).any():
        raise ValueError("Boxes to be rendered are not normalized." f"[boxes={boxes}]")

    # Plot either whole image with bounding box annotation,
    # or crop the predictions
    if crop:
        assert ndim == 1
        box = boxes
        img = img[box[1] : box[3], box[0] : box[2]].copy()
    else:
        if ndim == 1:
            boxes = [boxes]
            labels = [labels]
        for idx, box in enumerate(boxes):
            # TODO: Support for colors based on label
            # color = [int(c) for c in COCO_COLORS[labels[idx]]]
            color = (0, 255, 0)
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, thickness)
            text = f"{labels[idx]}"
            cv2.putText(
                img,
                text,
                (box[0], box[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2,
            )
    return img


def gallery(
    items: List[str],
    formatter: Callable[[str, Optional[int]], str],
):
    """Shows a set of images in a gallery that flexes with the width of the notebook.

    Args:
        images (List[str]): URLs or bytes of images to display
        formatter (Callable[[str, Optional[int]], str]): A function callable that returns the nredered HTML.

    Returns:
        IPython.core.display.HTML: HTML object to display in Jupyter Notebook.
    """
    figures = [
        f"""<figure style="margin: 1px !important;">{formatter(item)}</figure>"""
        for _, item in enumerate(items)
    ]
    return HTML(
        data=f"""
        <div style="display: flex; flex-flow: row wrap; text-align: center;">
        {''.join(figures)}
        </div>
    """
    )
