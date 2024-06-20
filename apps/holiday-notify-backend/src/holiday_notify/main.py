from __future__ import annotations

import logging

log = logging.getLogger("holiday_notify")

from holiday_notify import nager_date
from holiday_notify.core import settings
from holiday_notify.database import db_settings
from holiday_notify.domain import NagerAPI
from holiday_notify.helpers import http_helpers
from holiday_notify.setup import setup_db, setup_logging

import hishel
import httpx
import red_logging
from red_utils.ext import httpx_utils, sqlalchemy_utils
from sqlalchemy.exc import IntegrityError

if __name__ == "__main__":
    setup_logging()
    setup_db()

    # all_countries: NagerAPI.nager_country.ListNagerCountryMetas = (
    #     nager_date.country.get_all_countries_meta()
    # )
    # log.debug(f"Retrieved [{all_countries.count}] country/countries.")

    # country_info: NagerAPI.NagerCountry = nager_date.country.get_country_info(
    #     country_code="RU"
    # )
    # log.debug(f"Country info (schema): {country_info}")

    try:
        countries = nager_date.country.get_all_countries_borders()
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting all countries and their borders. Details: {exc}"
        )
        log.error(msg)

        raise exc
