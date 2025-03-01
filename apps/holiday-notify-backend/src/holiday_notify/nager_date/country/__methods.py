from __future__ import annotations

import json
import logging
import typing as t
import time

log = logging.getLogger("holiday_notify.nager_date.country.methods")

from holiday_notify.database import DBSettings, db_settings
from holiday_notify.domain import NagerAPI
from holiday_notify.helpers import http_helpers
from holiday_notify.nager_date.constants import BASE_URL
from holiday_notify.nager_date.endpoints import AVAILABLE_COUNTRIES, COUNTRY_INFO

import httpx
from red_utils.ext import httpx_utils, sqlalchemy_utils
from sqlalchemy.exc import IntegrityError
from red_utils.ext.context_managers import cli_spinners


def add_countries_meta_to_database(
    db_settings: DBSettings = db_settings,
    models: list[NagerAPI.NagerCountryMetaModel] = None,
):
    return_dict: dict[
        str,
        list[
            t.Union[
                NagerAPI.NagerCountryMetaModel,
                dict[str, t.Union[str, NagerAPI.NagerCountryMetaModel]],
            ]
        ],
    ] = {
        "successes": [],
        "errors": [],
        "skipped": [],
    }

    session_pool = db_settings.get_session_pool()

    with session_pool() as session:
        repo = NagerAPI.NagerCountryMetaRepository(session=session)

        for m in models:
            try:
                existing_model: NagerAPI.NagerCountryMetaModel = (
                    repo.get_by_country_code(country_code=m.countryCode)
                )
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception checking for country '{m.name}' in database. Details: {exc}"
                )
                log.error(msg)

                return_dict["errors"].append(
                    {"exc_type": f"{type(exc)}", "details": f"{exc}", "model": m}
                )

                # raise exc
                continue

            if existing_model:
                log.debug(f"Country '{m.name}' already exists in database. Skipping.")
                return_dict["skipped"].append(existing_model)

                continue

            else:
                try:
                    repo.add(m)

                    return_dict["successes"].append(m)
                except IntegrityError as integ_err:
                    msg = Exception(f"Country '{m.name}' already exists in database.")
                    log.warning(msg)

                    return_dict["skippd"].append(m)

                    continue
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception committing country '{m.name}' to database. Details: {exc}"
                    )
                    log.error(msg)

                    return_dict["errors"].append(m)

                    continue

        return return_dict


def get_all_countries_meta(
    controller: httpx_utils.HishelCacheClientController = http_helpers.HTTP_CONTROLLER,
) -> NagerAPI.nager_country.ListNagerCountryMetas:
    request: httpx.Request = httpx_utils.build_request(
        url=f"{BASE_URL}/{AVAILABLE_COUNTRIES}"
    )

    log.info(f"Requesting {request.url}")
    with controller as http_ctl:
        res = http_ctl.send_request(request)

        log.info(f"Countries response: [{res.status_code}: {res.reason_phrase}]")

        if not res.status_code == 200:
            log.warning(
                f"Non-200 response: [{res.status_code}: {res.reason_phrase}]: {res.text}"
            )

        res_decoded = http_ctl.decode_res_content(res=res)
        # log.debug(f"Decoded response ({type(res_decoded)}): {res_decoded}")

        country_list = NagerAPI.nager_country.ListNagerCountryMetas(
            countries=res_decoded
        )
        # log.debug(f"Countries: {country_list.countries}")

    models: list[NagerAPI.NagerCountryMetaModel] = []
    for c in country_list.countries:
        try:
            country_model = NagerAPI.NagerCountryMetaModel(
                name=c.name, countryCode=c.countryCode
            )
            models.append(country_model)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception converting country '{c.name}' schema to database model. Details: {exc}"
            )
            log.error(msg)

            continue

    try:
        models_to_db = add_countries_meta_to_database(models=models)
        # log.debug(f"Add models to DB results: {models_to_db}")
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception adding country model(s) to the database. Details: {exc}"
        )
        log.error(msg)

        raise exc

    if len(models_to_db["errors"]) > 0:
        log.warning(
            f"Encountered [{len(models_to_db['errors'])}] error(s): {models_to_db['errors']}"
        )

    return country_list


def add_country_info_to_database(
    country_info: NagerAPI.NagerCountry = None, db_settings: DBSettings = db_settings
):
    try:
        country_info_model = NagerAPI.NagerCountryModel(
            commonName=country_info.commonName,
            officialName=country_info.officialName,
            countryCode=country_info.countryCode,
            region=country_info.countryCode,
        )

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception converting country schema to database model. Details: {exc}"
        )
        log.error(msg)

        raise exc

    session_pool = db_settings.get_session_pool()

    if country_info.borders:
        with session_pool() as session:
            repo = NagerAPI.NagerCountryRepository(session=session)
            for border_country in country_info.borders:
                border_model: NagerAPI.NagerCountryModel = repo.get_by_country_code(
                    country_code=border_country.countryCode
                )

                if not border_model:
                    log.debug(
                        f"Border country '{border_country.commonName}' not found in database. Adding to model"
                    )
                    border_model = NagerAPI.NagerCountryModel(
                        commonName=border_country.commonName,
                        officialName=border_country.officialName,
                        countryCode=border_country.countryCode,
                        region=border_country.region,
                    )
                else:
                    log.warning(
                        f"Border country '{border_country.commonName},' bordering '{country_info.commonName},' already exists in the database. Skipping."
                    )
                    continue

                country_info_model.borders.append(border_model)

            try:
                repo.add(country_info_model)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception saving country '{country_info_model.commonName}' to database. Details: {exc}"
                )
                log.error(msg)

                raise exc


def get_country_info(
    country_code: str = None,
    controller: httpx_utils.HishelCacheClientController = http_helpers.HTTP_CONTROLLER,
):
    request: httpx.Request = httpx_utils.build_request(
        url=f"{BASE_URL}/{COUNTRY_INFO}/{country_code}"
    )

    log.info(f"Requesting {request.url}")
    with controller as http_ctl:
        res = http_ctl.send_request(request)

        log.info(f"Countries response: [{res.status_code}: {res.reason_phrase}]")

        if not res.status_code == 200:
            log.warning(
                f"Non-200 response: [{res.status_code}: {res.reason_phrase}]: {res.text}"
            )

        res_decoded: dict = http_ctl.decode_res_content(res=res)
        # log.debug(f"Decoded response ({type(res_decoded)}): {res_decoded}")

        country_info: NagerAPI.NagerCountry = NagerAPI.NagerCountry.model_validate(
            res_decoded
        )
        # log.debug(f"Country info: {country_info}")

    try:
        country_info_model: NagerAPI.NagerCountryModel = (
            NagerAPI.nager_country.country_info_schema_to_model(
                country_schema=country_info
            )
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception converting country info schema to database model. Details: {exc}"
        )
        log.error(msg)

        raise exc

    # log.debug(f"Country info model: {country_info_model.__dict__}")

    return country_info


def get_all_countries_borders(
    request_pause: int | None = 5,
) -> list[NagerAPI.NagerCountry]:
    log.info("Getting all countries and their borders")
    try:
        all_country_metas: NagerAPI.nager_country.ListNagerCountryMetas = (
            get_all_countries_meta()
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting all country metadata. Details: {exc}"
        )
        log.error(msg)

        raise exc

    assert (
        isinstance(all_country_metas.countries, list)
        and len(all_country_metas.countries) > 0
    ), ValueError(
        f"all_country_metas.countries should be a non-empty list of countries. Got type: ({type(all_country_metas.countries)})"
    )

    country_info_objs: list[NagerAPI.NagerCountry] = []

    for _country_meta in all_country_metas.countries:
        try:
            country_info: NagerAPI.NagerCountry = get_country_info(
                country_code=_country_meta.countryCode
            )
            country_info_objs.append(country_info)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting country information for country '{_country_meta.name}'. Details: {exc}"
            )
            log.error(msg)

            continue

        if request_pause:
            assert isinstance(request_pause, int) and request_pause > 0, TypeError(
                f"Request pause must be a non-zero integer"
            )
            log.debug(f"Pausing for [{request_pause}] second(s) between requests")
            with cli_spinners.SimpleSpinner(
                message=f"Pausing [{request_pause}] second(s) between requests ..."
            ):
                time.sleep(5)

    return country_info_objs
