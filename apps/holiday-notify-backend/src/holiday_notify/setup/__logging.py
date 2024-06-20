import logging

log = logging.getLogger("holiday_notify.setup").setLevel(logging.WARNING)

from holiday_notify.core import AppSettings, settings

import red_logging

DISABLE_LOGGERS: list[str] = ["httpx", "httpcore", "chardet", "sqlalchemy"]


def setup_logging(
    app_name: str = "holiday_notify",
    settings: AppSettings = settings,
    disable_existing_loggers: bool = False,
    disable_logger_names: list[str] = DISABLE_LOGGERS,
):
    try:
        red_logging.setup_logging(
            app_name=app_name,
            log_level=settings.log_level,
            disable_existing_loggers=disable_existing_loggers,
            disable_logger_names=disable_logger_names,
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception setting up logging for app '{app_name}'. Details: {exc}"
        )
        log.error(msg)

        raise exc
