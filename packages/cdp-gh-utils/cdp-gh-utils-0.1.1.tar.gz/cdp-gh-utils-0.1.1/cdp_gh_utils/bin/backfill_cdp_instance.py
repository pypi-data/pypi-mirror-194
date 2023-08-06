#!/usr/bin/env python

import argparse
import logging
import sys
import traceback
from pathlib import Path

from cdp_gh_utils import actions

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


class Args(argparse.Namespace):
    def __init__(self) -> None:
        self.__parse()

    def __parse(self) -> None:
        p = argparse.ArgumentParser(
            prog="backfill-cdp-instance",
            description=(
                "Iteratively triggers the Event Gather Pipeline workflow via "
                "GitHub Actions to backfill a CDP instance. Only one workflow run "
                "will ever happen at a single time."
            ),
        )
        p.add_argument(
            "owner",
            type=str,
            help="The organization which hosts the instance. i.e. 'CouncilDataProject'",
        )
        p.add_argument(
            "repo",
            type=str,
            help="The organization which hosts the instance. i.e. 'seattle'",
        )
        p.add_argument(
            "start_datetime",
            type=str,
            help="The start datetime of the backfill in ISO format. i.e. '2022-01-01'",
        )
        p.add_argument(
            "end_datetime",
            type=str,
            help="The end datetime of the backfill in ISO format. i.e. '2023-01-01'",
        )
        p.add_argument(
            "--outfile",
            type=Path,
            default=None,
            help="Path to the where the backfill results should be stored to CSV.",
        )
        p.add_argument(
            "--iter_days",
            type=int,
            default=3,
            help="The number of days to backfill during each workflow run. Default: 3",
        )
        p.add_argument(
            "--overlap_days",
            type=int,
            default=1,
            help="The number of days to overlap each workflow run by. Default: 1",
        )
        p.add_argument(
            "--token",
            type=str,
            default=None,
            help="GitHub Personal Access Token to use for initializing workflow runs.",
        )
        p.add_argument(
            "--workflow_filename",
            type=str,
            default="event-gather-pipeline.yml",
            help=(
                "The name of the workflow file which acts as the "
                "event gather pipeline action definition. "
                "Default: 'event-gather-pipeline.yml'"
            ),
        )
        p.add_argument(
            "--ref",
            type=str,
            default="main",
            help=(
                "The branch or git ref name to trigger the workflow on. "
                "Default: 'main'"
            ),
        )
        p.add_argument(
            "--ignore_errors",
            action="store_true",
            help=(
                "Try to backfill all batches regardless of errors. "
                "Note: The status of all workflow runs is stored to CSV "
                "enabling later workflow re-running."
            ),
        )
        p.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            help="Run with debug logging.",
        )
        p.parse_args(namespace=self)


def main() -> None:
    # Get args
    args = Args()

    # Determine log level
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Setup logging
    logging.basicConfig(
        level=log_level,
        format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
    )

    # Process
    try:
        results = actions.backfill_instance(
            owner=args.owner,
            repo=args.repo,
            start_datetime=args.start_datetime,
            end_datetime=args.end_datetime,
            iter_days=args.iter_days,
            overlap_days=args.overlap_days,
            ignore_errors=args.ignore_errors,
            token=args.token,
            workflow_filename=args.workflow_filename,
            ref=args.ref,
        )

        # Handle storage
        if args.outfile:
            results_save_path = args.outfile
        else:
            results_save_path = Path(
                f"cdp-backfill-results"
                f"--{args.owner}-{args.repo}"
                f"--{args.start_datetime}-{args.end_datetime}.csv"
            )

        # Store results
        results.to_csv(results_save_path, index=False)

    except Exception as e:
        log.error("=============================================")
        log.error("\n\n" + traceback.format_exc())
        log.error("=============================================")
        log.error("\n\n" + str(e) + "\n")
        log.error("=============================================")
        sys.exit(1)


###############################################################################
# Allow caller to directly run this module (usually in development scenarios)

if __name__ == "__main__":
    main()
