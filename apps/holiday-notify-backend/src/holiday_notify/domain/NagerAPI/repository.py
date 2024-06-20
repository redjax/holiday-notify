from __future__ import annotations

import logging

log = logging.getLogger("holiday_notify.domain.NagerAPI.repository")

from .models import (
    NagerCountryMetaModel,
    NagerCountryMetaRepositoryBase,
    NagerCountryModel,
    NagerCountryRepositoryBase,
)

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
import sqlalchemy.orm as so

class NagerCountryMetaRepository(NagerCountryMetaRepositoryBase):
    def __init__(self, session: so.Session) -> None:  # noqa: D107
        assert session is not None, ValueError("session cannot be None")
        assert isinstance(session, so.Session), TypeError(
            f"session must be of type sqlalchemy.orm.Session. Got type: ({type(session)})"
        )

        self.session: so.Session = session

    def add(self, entity: NagerCountryMetaModel) -> None:
        """Add new entity to the database."""
        try:
            self.session.add(instance=entity)
            self.session.commit()
        except IntegrityError as integ:
            msg = Exception(
                f"Integrity error committing entity to database. Details: {integ}"
            )
            log.warning(msg)

            raise integ
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception committing entity to database. Details: {exc}"
            )

            raise msg

    def remove(self, entity: NagerCountryMetaModel) -> None:
        """Remove existing entity from the database."""
        try:
            self.session.delete(instance=entity)
            self.session.commit()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception removing entity from database. Details: {exc}"
            )
            log.error(msg)

            raise msg

    def get_by_id(self, country_id: int) -> NagerCountryMetaModel | None:
        return (
            self.session.query(NagerCountryMetaModel)
            .filter(NagerCountryMetaModel.country_meta_id == country_id)
            .first()
        )

    def get_all_country_names(self) -> list[int]:
        """Return a list of all country names in database entitites."""
        try:
            all_countries: list[NagerCountryMetaModel] = self.session.query(
                NagerCountryMetaModel
            ).all()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting all country names from database. Details: {exc}"
            )
            log.error(msg)

            raise msg

        country_names: list[str] = []

        for _country in all_countries:
            country_names.append(_country.name)

        return country_names

    def get_all_country_codes(self) -> list[int]:
        """Return a list of all country codes in database entitites."""
        try:
            all_countries: list[NagerCountryMetaModel] = self.session.query(
                NagerCountryMetaModel
            ).all()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting all country codes from database. Details: {exc}"
            )
            log.error(msg)

            raise msg

        country_codes: list[str] = []

        for _country in all_countries:
            country_codes.append(_country.countryCode)

        return country_codes

    def get_all(self) -> list[NagerCountryMetaModel]:
        """Return a list of all entitites found in database."""
        try:
            all_comics: list[NagerCountryMetaModel] = self.session.query(
                NagerCountryMetaModel
            ).all()

            return all_comics
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting all countries from database. Details: {exc}"
            )
            log.error(msg)

            raise msg

    def get_by_id(self, country_meta_id: int) -> NagerCountryMetaModel:
        try:
            return self.session.query(NagerCountryMetaModel).get(country_meta_id)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception retrieving entity by ID '{country_meta_id}'. Details: {exc}"
            )
            log.error(msg)

            raise msg

    def get_by_name(self, country_name: int) -> NagerCountryMetaModel:
        try:
            return (
                self.session.query(NagerCountryMetaModel)
                .filter_by(name=country_name)
                .one_or_none()
            )
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception retrieving entity by country name '{country_name}'. Details: {exc}"
            )
            log.error(msg)
            raise msg

    def get_by_country_code(self, country_code: str) -> NagerCountryMetaModel:
        try:
            return (
                self.session.query(NagerCountryMetaModel)
                .filter_by(countryCode=country_code)
                .one_or_none()
            )
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception retrieving entity by country code '{country_code}'. Details: {exc}"
            )
            log.error(msg)
            raise msg

    def count(self) -> int:
        try:
            return self.session.query(NagerCountryMetaModel).count()
        except Exception as exc:
            msg = Exception(f"Unhandled exception counting entities. Details: {exc}")
            log.error(msg)

            raise msg


class NagerCountryRepository(NagerCountryRepositoryBase):
    def __init__(self, session: so.Session) -> None:  # noqa: D107
        assert session is not None, ValueError("session cannot be None")
        assert isinstance(session, so.Session), TypeError(
            f"session must be of type sqlalchemy.orm.Session. Got type: ({type(session)})"
        )

        self.session: so.Session = session

    def add(self, entity: NagerCountryModel) -> None:
        """Add new entity to the database."""
        try:
            self.session.add(instance=entity)
            self.session.commit()
        except IntegrityError as integ:
            msg = Exception(
                f"Integrity error committing entity to database. Details: {integ}"
            )
            log.warning(msg)

            raise integ
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception committing entity to database. Details: {exc}"
            )

            raise msg

    def remove(self, entity: NagerCountryModel) -> None:
        """Remove existing entity from the database."""
        try:
            self.session.delete(instance=entity)
            self.session.commit()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception removing entity from database. Details: {exc}"
            )
            log.error(msg)

            raise msg

    def get_by_id(self, country_id: int) -> NagerCountryModel:
        try:
            return self.session.query(NagerCountryModel).get(country_id)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception retrieving entity by ID '{country_id}'. Details: {exc}"
            )
            log.error(msg)

            raise msg

    def get_by_name(self, country_name: int) -> NagerCountryModel:
        try:
            return (
                self.session.query(NagerCountryModel)
                .filter_by(name=country_name)
                .one_or_none()
            )
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception retrieving entity by country name '{country_name}'. Details: {exc}"
            )
            log.error(msg)
            raise msg

    def get_by_country_code(self, country_code: str) -> NagerCountryModel:
        try:
            return (
                self.session.query(NagerCountryModel)
                .filter_by(countryCode=country_code)
                .one_or_none()
            )
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception retrieving entity by country code '{country_code}'. Details: {exc}"
            )
            log.error(msg)
            raise msg

    def get_all_country_names(self) -> list[int]:
        """Return a list of all country names in database entitites."""
        try:
            all_countries: list[NagerCountryModel] = self.session.query(
                NagerCountryModel
            ).all()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting all country names from database. Details: {exc}"
            )
            log.error(msg)

            raise msg

        country_names: list[str] = []

        for _country in all_countries:
            country_names.append(_country.officialName)

        return country_names

    def get_all_country_codes(self) -> list[int]:
        """Return a list of all country codes in database entitites."""
        try:
            all_countries: list[NagerCountryModel] = self.session.query(
                NagerCountryModel
            ).all()
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting all country codes from database. Details: {exc}"
            )
            log.error(msg)

            raise msg

        country_codes: list[str] = []

        for _country in all_countries:
            country_codes.append(_country.countryCode)

        return country_codes

    def get_all(self) -> list[NagerCountryModel]:
        """Return a list of all entitites found in database."""
        try:
            all_comics: list[NagerCountryModel] = self.session.query(
                NagerCountryModel
            ).all()

            return all_comics
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting all countries from database. Details: {exc}"
            )
            log.error(msg)

            raise msg

    def count(self) -> int:
        try:
            return self.session.query(NagerCountryModel).count()
        except Exception as exc:
            msg = Exception(f"Unhandled exception counting entities. Details: {exc}")
            log.error(msg)

            raise msg
