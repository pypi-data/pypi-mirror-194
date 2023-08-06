"""Top-level package for cdp_gh_utils."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cdp-gh-utils")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Eva Maxfield Brown"
__email__ = "evamaxfieldbrown@gmail.com"
