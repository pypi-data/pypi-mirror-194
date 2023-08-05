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

```bash
backfill-cdp-instance evamaxfield cdp-dev 2023-02-01 2023-03-01
```

## Documentation

For full package documentation please visit [CouncilDataProject.github.io/cdp-gh-utils](https://CouncilDataProject.github.io/cdp-gh-utils).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

**MIT License**
