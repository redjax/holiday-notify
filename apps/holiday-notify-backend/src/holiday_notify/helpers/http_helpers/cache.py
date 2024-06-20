from __future__ import annotations

import logging
from pathlib import Path
import typing as t

log = logging.getLogger("holiday_notify.helpers.http_helpers")

from red_utils.ext import httpx_utils

def get_cache_client_controller(
    cache_dir: t.Union[str, Path] = None, ttl: int = 900, force_cache: bool = False
) -> httpx_utils.HishelCacheClientController:
    try:
        _controller: httpx_utils.HishelCacheClientController = (
            httpx_utils.HishelCacheClientController(
                force_cache=force_cache,
                storage=httpx_utils.get_hishel_file_storage(
                    cache_dir=cache_dir, ttl=ttl
                ),
            )
        )

        return _controller
    except Exception as exc:
        msg = Exception(f"Unhandled exception initializing controller. Details: {exc}")
        log.error(msg)

        raise exc


HTTP_CONTROLLER: httpx_utils.HishelCacheClientController = get_cache_client_controller(
    cache_dir=".data/cache/http", ttl=900, force_cache=True
)
