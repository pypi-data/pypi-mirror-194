# Copyright 2022- Autonomi AI, Inc. All rights reserved.
import time
from typing import List

import pandas as pd
import tenacity
from loguru import logger

from autonomi.client._client import BaseClient
from autonomi.client.constants import StoreMetadata
from autonomi.client.utils import apply_parallel

retry = tenacity.retry(
    stop=tenacity.stop.stop_after_attempt(5), wait=tenacity.wait.wait_fixed(5)
)


class JobsClient(BaseClient):
    """Client for the Jobs API."""

    DEFAULT_TIMEOUT_SEC = 180

    def info(self, id: str) -> dict:
        """Get the status of a single job.

        Args:
            id (str): The job id.

        Returns:
            dict: The job info.
        """
        json_response = self._connection.get(
            route=f"{id}",
            timeout=JobsClient.DEFAULT_TIMEOUT_SEC,
        )
        return json_response

    def list(self, offset: int = 0, limit: int = 10) -> dict:
        """List recent jobs.

        Returns:
            List[JobMetadata]: List of recent jobs and their metadata.
        """
        json_response = self._connection.get(
            route="",
            params=dict(offset=offset, limit=limit),
            timeout=JobsClient.DEFAULT_TIMEOUT_SEC,
        )
        return json_response

    def submit(self, task: str, url: str, frame_index: int = 0) -> dict:
        """Submit a single task to the Jobs API.

        Args:
            task (str): The task to run.
            url (str): The URL of the video to run the task on.
            frame_index (int, optional): The frame index to run the task on. Defaults to 0.

        Returns:
            dict: The job info.
        """
        json_data = dict(task=task, url=url, frame_index=int(frame_index))
        logger.info(f"job submit [data={json_data}]")
        json_response = self._connection.post(
            route="submit",
            json=json_data,
            timeout=JobsClient.DEFAULT_TIMEOUT_SEC,
        )
        print(f"✅Job submit complete [response={json_response}]")
        return json_response

    def batch_submit(
        self,
        results_df: pd.DataFrame,
        tasks: List[str] = None,
        threads: int = 0,
    ) -> pd.DataFrame:
        """Submit a batch of jobs to the Jobs API.

        Args:
            results_df (pd.DataFrame): The dataframe to submit jobs for.
            tasks (List[str], optional): The list of tasks to run. Defaults to None.
            threads (int, optional): The number of threads to use. Defaults to 0.

        Returns:
            pd.DataFrame: The dataframe with the job info.
        """
        df = results_df.copy()

        # Check dataframe entities
        for column in [
            StoreMetadata.FILE_ID,
            StoreMetadata.FRAME_ID,
        ]:
            if column not in df.columns:
                raise ValueError(f"column unavailable [column={column}]")

        # Check task availability
        if tasks is None:
            tasks = self.available_tasks()
        else:
            for task in tasks:
                if task not in self.available_tasks():
                    raise ValueError(f"task unavailable [task={task}]")

        # Submit all tasks for all rows
        for task in tasks:

            def _submit_one(row):
                "Submit single task at a time"
                try:
                    response = self.submit(
                        task,
                        url=str(row[StoreMetadata.FILE_URL]),
                        frame_index=int(row[StoreMetadata.FRAME_ID]),
                    )
                    # TODO: Get the appropriate response id
                    return response["request"]["id"]
                except Exception as exc:
                    logger.debug(
                        f"Failed to submit task [task={task}, row={row}, exc={exc}]"
                    )
                    return None

            df[f"{task}_job_id"] = apply_parallel(df, _submit_one, threads=threads)

        print(f"🚀 Submitted {len(tasks) * len(df)} tasks.")
        return df

    def batch_status(self, df: pd.DataFrame, wait_until_finish: bool = True):
        """Fetch batch job results via API.
        Optionally, block on completion of all jobs.
        """
        # Keep polling job info for all cells with `*_job_id`
        pending, total = 0, 0
        for column in df.columns:
            if not column.endswith("_job_id"):
                continue
            status = df[column].apply(lambda x: self._handle_one(x))
            pending += (status == "RUNNING").sum()
            total += len(status)

        if wait_until_finish:
            while pending:
                print(f"pending/total = {pending}/{total}")
                time.sleep(10)
                pending, total = self.job_status(df)
        return pending, total

    def _handle_one(self, id: str):
        """Fetch job artifacts for a single job id, once it succeeds."""
        response = self.job_info(id)
        if response["status"] != "SUCCESSFUL":
            return response["status"]
        try:
            artifacts = response["response"]["artifacts"]
            return artifacts[0]
        except Exception:
            logger.debug(f"Failed to fetch artifacts for job_id={id}")
            return None
