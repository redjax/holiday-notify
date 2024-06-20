from __future__ import annotations

import logging

log = logging.getLogger("holidy_notify.domain.NagerAPI.methods")

from holiday_notify.database import DBSettings, db_settings
from holiday_notify.domain import NagerAPI

from red_utils.ext import sqlalchemy_utils
from sqlalchemy.exc import IntegrityError, NoResultFound

def get_or_create_border_country(
    border_country: NagerAPI.NagerBorderCountry = None,
    db_settings: DBSettings = db_settings,
) -> NagerAPI.NagerCountryModel:
    """Get existing border country model from database, or create if one does not exist."""
    with sqlalchemy_utils.get_session_pool(
        engine=db_settings.get_engine()
    )() as session:

        border_model = (
            session.query(NagerAPI.NagerCountryModel)
            .filter_by(
                commonName=border_country.commonName,
                officialName=border_country.officialName,
                countryCode=border_country.countryCode,
                region=border_country.region,
            )
            .first()
        )

    if not border_model:
        border_model = NagerAPI.NagerCountryModel(
            commonName=border_country.commonName,
            officialName=border_country.officialName,
            countryCode=border_country.countryCode,
            region=border_country.region,
        )
        session.add(border_model)
        session.commit()
        session.refresh(border_model)

    return border_model


def country_info_schema_to_model(
    country_schema: NagerAPI.NagerCountry = None,
) -> NagerAPI.NagerCountryModel:
    """Convert a country information Pydantic schema to a SQLAlchemy model."""
    session_pool = db_settings.get_session_pool()

    with session_pool() as session:
        repo = NagerAPI.NagerCountryRepository(session=session)

        db_country_model = repo.get_by_country_code(country_schema.countryCode)

        if not db_country_model:
            country_model = NagerAPI.NagerCountryModel(
                commonName=country_schema.commonName,
                officialName=country_schema.officialName,
                countryCode=country_schema.countryCode,
                region=country_schema.region,
            )

            try:
                repo.add(entity=country_model)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception adding country info model to database. Details: {exc}"
                )
                log.error(msg)

                raise exc

    if country_schema.borders:
        with session_pool() as session:
            repo = NagerAPI.NagerCountryRepository(session=session)

            db_country_model: NagerAPI.NagerCountryModel = repo.get_by_country_code(
                country_schema.countryCode
            )

            if not db_country_model:
                raise NoResultFound

            country_model = NagerAPI.NagerCountryModel(
                commonName=country_schema.commonName,
                officialName=country_schema.officialName,
                countryCode=country_schema.countryCode,
                region=country_schema.region,
            )

            for border_country in country_schema.borders:
                border_model = get_or_create_border_country(
                    border_country=border_country
                )
                if border_model not in db_country_model.borders:
                    country_model.borders.append(border_model)
                    # repo.session.commit()
                    try:
                        repo.add(entity=db_country_model)
                    except Exception as exc:
                        msg = Exception(
                            f"Unhandled exception appending borders to country '{db_country_model.commonName}'. Details: {exc}"
                        )
                        log.error(msg)

                    # repo.session.refresh(country_model)

    return country_model
