import logging

log = logging.getLogger("holidy_notify.helpers.cache_helpers")

import typing as t
from pathlib import Path
from red_utils.ext import diskcache_utils

import diskcache


def new_cache_controller(
    cache_directory: t.Union[str, Path] = None,
    cache_timeout: int = 60,
    cache_disk: t.ClassVar[diskcache].Cache = diskcache.Cache,
    index: bool = False,
):
    try:
        ctl: diskcache_utils.DiskCacheController = diskcache_utils.DiskCacheController(
            cache_directory=cache_directory,
            cache_timeout=cache_timeout,
            cache_disk=cache_disk,
            index=index,
        )

        return ctl
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception initializing DiskCache Cache controller. Details: {exc}"
        )
        log.error(msg)

        raise exc
