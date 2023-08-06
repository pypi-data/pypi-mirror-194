#!/usr/bin/env python

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from fastcore.net import HTTP4xxClientError
from ghapi.all import GhApi
from tqdm import tqdm

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


def backfill_instance(  # noqa: C901
    owner: str,
    repo: str,
    start_datetime: str | datetime,
    end_datetime: str | datetime,
    iter_days: int | timedelta = 3,
    overlap_days: int | timedelta = 1,
    ignore_errors: bool = False,
    token: str | None = None,
    workflow_filename: str = "event-gather-pipeline.yml",
    ref: str = "main",
) -> pd.DataFrame:
    if token:
        # Create API
        api = GhApi(token=token)

    else:
        # Check for token
        if "GITHUB_TOKEN" not in os.environ:
            load_dotenv()
        if "GITHUB_TOKEN" not in os.environ:
            raise OSError("No GitHub Token found.")

        # Init api
        api = GhApi()

    # Create or convert datetimes
    if isinstance(start_datetime, str):
        start_datetime = datetime.fromisoformat(start_datetime)
    if isinstance(end_datetime, str):
        end_datetime = datetime.fromisoformat(end_datetime)
    if isinstance(iter_days, int):
        iter_days = timedelta(days=iter_days)
    if isinstance(overlap_days, int):
        overlap_days = timedelta(days=overlap_days)

    # Create all of the parameter sets
    datetimes = []
    this_iter_start = start_datetime
    while this_iter_start < end_datetime:
        this_iter_end = this_iter_start + iter_days
        datetimes.append((this_iter_start, this_iter_end))
        this_iter_start = this_iter_end - overlap_days

    # Log length
    log.info(
        f"Will backfill: "
        f"{start_datetime.isoformat()} - {end_datetime.isoformat()} "
        f"in {len(datetimes)} batches"
    )

    # Backfill
    backfill_results = []
    for this_iter_start, this_iter_end in tqdm(datetimes, desc="Backfill"):
        iter_start_str = this_iter_start.isoformat()
        iter_end_str = this_iter_end.isoformat()
        log.info(f"Backfilling: {iter_start_str} - {iter_end_str}")

        # Actual run
        try:
            # Trigger the run
            log.debug("Triggering new workflow run.")
            api.actions.create_workflow_dispatch(
                owner=owner,
                repo=repo,
                workflow_id=workflow_filename,
                ref=ref,
                inputs={
                    "from": iter_start_str,
                    "to": iter_end_str,
                },
            )

            # Find the new run
            found_run = False
            max_iter = 20
            current_iter = 0
            while not found_run and current_iter < max_iter:
                log.debug("Checking for queued workflow run.")
                queued_runs = api.actions.list_workflow_runs(
                    owner=owner,
                    repo=repo,
                    workflow_id=workflow_filename,
                    branch=ref,
                    event="workflow_dispatch",
                    status="queued",
                )
                if len(queued_runs["workflow_runs"]) == 1:
                    log.debug("Found the queued workflow run.")
                    found_run = True
                    break
                else:
                    current_iter += 1
                    time.sleep(0.5)

            # Handle not found
            if not found_run:
                raise ValueError("Could not find queued run.")

            # Find the workflow to monitor
            watch_workflow_id = queued_runs["workflow_runs"][0]["id"]

            # Keep checking status
            workflow_complete = False
            log.debug("Watching workflow run.")
            while not workflow_complete:
                workflow_details = api.actions.get_workflow_run(
                    owner=owner,
                    repo=repo,
                    run_id=watch_workflow_id,
                )

                # Check status
                if workflow_details["status"] == "completed":
                    workflow_complete = True
                    log.debug("Workflow complete.")
                    break
                else:
                    time.sleep(60)

            # Check conclusion
            workflow_link = (
                f"https://github.com/{owner}/{repo}/actions/runs/{watch_workflow_id}"
            )
            if workflow_details["conclusion"] != "success":
                msg = f"Workflow completed but did not end in sucess. ({workflow_link})"
                log.error(msg)
                if not ignore_errors:
                    raise ValueError(msg)

            # Add result
            backfill_results.append(
                {
                    "start_datetime": iter_start_str,
                    "end_datetime": iter_end_str,
                    "workflow_id": watch_workflow_id,
                    "workflow_link": workflow_link,
                    "status": workflow_details["status"],
                    "conclusion": workflow_details["conclusion"],
                    "error": None,
                }
            )

        except (HTTP4xxClientError, ValueError) as e:
            log.error(f"Failed during {iter_start_str} - {iter_end_str}")
            log.error(e)

            if not ignore_errors:
                raise e

            # Add result
            backfill_results.append(
                {
                    "start_datetime": iter_start_str,
                    "end_datetime": iter_end_str,
                    "workflow_id": None,
                    "workflow_link": None,
                    "status": "failed_start",
                    "conclusion": "failed_start",
                    "error": str(e),
                }
            )

    return pd.DataFrame(backfill_results)
