# cdp-gh-utils

[![Build Status](https://github.com/CouncilDataProject/cdp-gh-utils/workflows/CI/badge.svg)](https://github.com/CouncilDataProject/cdp-gh-utils/actions)
[![Documentation](https://github.com/CouncilDataProject/cdp-gh-utils/workflows/Documentation/badge.svg)](https://CouncilDataProject.github.io/cdp-gh-utils)

Utility functions and scripts to manage CDP (and other) GitHub repositories.

---

## Installation

**Stable Release:** `pip install cdp-gh-utils`<br>
**Development Head:** `pip install git+https://github.com/CouncilDataProject/cdp-gh-utils.git`

## Backfilling Instances

⚠️ ⚠️ Note: prior to using this library, be sure to create a 
[GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) 
and store it to a `GITHUB_TOKEN` environment variable (`.env` file also works). ⚠️ ⚠️


```
❯ backfill-cdp-instance -h

usage: backfill-cdp-instance [-h] [--outfile OUTFILE] [--iter_days ITER_DAYS] [--overlap_days OVERLAP_DAYS] [--token TOKEN] [--workflow_filename WORKFLOW_FILENAME] [--ref REF]
                             [--ignore_errors] [--debug]
                             owner repo start_datetime end_datetime

Iteratively triggers the Event Gather Pipeline workflow via GitHub Actions to backfill a CDP instance. Only one workflow run will ever happen at a single time.

positional arguments:
  owner                 The organization which hosts the instance. i.e. 'CouncilDataProject'
  repo                  The organization which hosts the instance. i.e. 'seattle'
  start_datetime        The start datetime of the backfill in ISO format. i.e. '2022-01-01'
  end_datetime          The end datetime of the backfill in ISO format. i.e. '2023-01-01'

options:
  -h, --help            show this help message and exit
  --outfile OUTFILE     Path to the where the backfill results should be stored to CSV.
  --iter_days ITER_DAYS
                        The number of days to backfill during each workflow run.
  --overlap_days OVERLAP_DAYS
                        The number of days to overlap each workflow run by.
  --token TOKEN         GitHub Personal Access Token to use for initializing workflow runs.
  --workflow_filename WORKFLOW_FILENAME
                        The name of the workflow file which acts as the event gather pipeline action definition.
  --ref REF             The branch or git ref name to trigger the workflow on.
  --ignore_errors       Try to backfill all batches regardless of errors.
  --debug               Run with debug logging.
```

```bash
backfill-cdp-instance evamaxfield cdp-dev 2023-02-01 2023-03-01
```

## Documentation

For full package documentation please visit [CouncilDataProject.github.io/cdp-gh-utils](https://CouncilDataProject.github.io/cdp-gh-utils).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

**MIT License**
