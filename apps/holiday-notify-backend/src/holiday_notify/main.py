import logging

log = logging.getLogger("holiday_notify")

from holiday_notify.core import settings
from holiday_notify.database import db_settings
from holiday_notify import nager_date

import httpx
import hishel
import red_logging
from red_utils.ext import httpx_utils
from red_utils.ext import sqlalchemy_utils
from holiday_notify.helpers import http_helpers
from sqlalchemy.exc import IntegrityError

from holiday_notify.domain import NagerAPI
from holiday_notify.setup import setup_logging, setup_db


if __name__ == "__main__":
    setup_logging()
    setup_db()

    # all_countries: ListNagerCountryMetas = nager_date.country.get_all_countries_meta()
    # log.debug(f"Retrieved [{all_countries.count}] country/countries.")

    country_info: NagerAPI.NagerCountry = nager_date.country.get_country_info(
        country_code="RU"
    )
    log.debug(f"Country info (schema): {country_info}")
