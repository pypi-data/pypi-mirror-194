# Copyright 2022- Autonomi AI, Inc. All rights reserved.
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from typing import Any, Callable, Dict, List, Union

import pandas as pd
from cloudpathlib import CloudPath


def apply_parallel(df: pd.DataFrame, func: Callable, threads: int = 0):
    """Apply a function to a DataFrame in parallel.

    Args:
        df: The DataFrame to apply the function to.
        func: The function to apply to each row of the DataFrame.
        threads: The number of threads to use. If 0, use all available threads.

    Returns:
        The DataFrame with the function applied to each row.
    """
    # if threads == 0:
    #     threads = None
    # with ThreadPoolExecutor(max_workers=threads) as executor:
    #     return pd.concat(executor.map(func, df.iterrows()), ignore_index=True)
    if threads > 0:
        # Multi-threaded thread-pool execution per-row
        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = list(executor.map(func, [row for _, row in df.iterrows()]))
        assert len(results) == len(df)
        return results
    else:
        # Single-threaded execution per-row
        return df.apply(lambda row: func(row), axis=1)


def as_dataframe(items: Union[Dict[Any, Any], List[Dict[Any, Any]]]) -> pd.DataFrame:
    """Convert a dict or list of dicts to a DataFrame.

    Args:
        data: The dict or list of dicts to convert to a DataFrame.

    Returns:
        The DataFrame.
    """
    if isinstance(items, list):
        return pd.DataFrame(items).convert_dtypes()
    elif isinstance(items, dict):
        return (
            pd.DataFrame.from_dict(items, orient="index").transpose().convert_dtypes()
        )
    else:
        raise ValueError(f"Unsupported type: {type(items)}")


def generate_presigned_s3_url(url: str, expire_seconds: int = 86400) -> str:
    """Generate a presigned URL for a given S3 URL.

    Args:
        url: The S3 URL to generate a presigned URL for.
        expire_seconds: The number of seconds the presigned URL should be valid for.

    Returns:
        The presigned URL.
    """
    path = CloudPath(url)
    client = path.client.client  # client: botocore.client.S3
    presigned_url: str = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": path.bucket, "Key": path.key},
        ExpiresIn=expire_seconds,
    )
    return presigned_url


def generate_presigned_gs_url(url: str, expire_seconds: int = 86400) -> str:
    """Generate a presigned URL for a given GCS URL.

    Args:
        url: The GCS URL to generate a presigned URL for.
        expire_seconds: The number of seconds the presigned URL should be valid for.

    Returns:
        The presigned URL.
    """
    path = CloudPath(url)
    client = path.client.client  # client: google.cloud.storage.client.Client
    bucket = client.get_bucket(path.bucket)
    blob = bucket.blob(path.blob)
    presigned_url: str = blob.generate_signed_url(
        version="v4", expiration=timedelta(seconds=expire_seconds), method="GET"
    )
    return presigned_url


def generate_presigned_url(url: str, expire_seconds: int = 86400) -> str:
    """Generate a presigned URL for a given URL.

    Args:
        url: The URL to generate a presigned URL for.
        expire_seconds: The number of seconds the presigned URL should be valid for.

    Returns:
        The presigned URL.
    """
    from urllib.parse import urlparse

    parsed_url = urlparse(url)
    if parsed_url.scheme == "s3":
        return generate_presigned_s3_url(url, expire_seconds)
    elif parsed_url.scheme == "gs":
        return generate_presigned_gs_url(url, expire_seconds)
    else:
        raise ValueError(f"Unsupported URL scheme [url={url}]")
