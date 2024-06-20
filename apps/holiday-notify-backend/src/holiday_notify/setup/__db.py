from __future__ import annotations

import logging

log = logging.getLogger("holiday_notify.setup.db")

from holiday_notify.database import DBSettings, db_settings
from holiday_notify.domain import NagerAPI

from red_utils.ext import sqlalchemy_utils
import sqlalchemy.orm as so

def setup_db(
    base_obj: so.DeclarativeBase = sqlalchemy_utils.Base,
    db_settings: DBSettings = db_settings,
):
    try:
        sqlalchemy_utils.create_base_metadata(
            base_obj=base_obj, engine=db_settings.get_engine()
        )
    except Exception as exc:
        msg = Exception(f"Unhandled exception initializing database. Details: {exc}")
        log.error(msg)

        raise exc
