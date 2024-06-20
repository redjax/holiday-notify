import logging

log = logging.getLogger("holiday_notify.domain.NagerAPI.models")

import typing as t
import abc

from red_utils.ext import sqlalchemy_utils
import sqlalchemy as sa
import sqlalchemy.orm as so


class NagerCountryMetaModel(sqlalchemy_utils.Base):
    __tablename__ = "country_meta"
    __table_args__ = (sa.UniqueConstraint("countryCode", name="_country_code_uc"),)

    country_meta_id: so.Mapped[sqlalchemy_utils.custom_types.INT_PK]
    name: so.Mapped[str] = so.mapped_column(sa.VARCHAR(255))
    countryCode: so.Mapped[str] = so.mapped_column(sa.VARCHAR(255))


class NagerCountryMetaRepositoryBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, entity: NagerCountryMetaModel):
        """Add new entity to repository."""
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: NagerCountryMetaModel):
        """Remove existing entity from repository."""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, comic_id: int) -> NagerCountryMetaModel:
        """Retrieve entity from repository by its ID."""
        raise NotImplementedError()


class NagerCountryModelBase(sqlalchemy_utils.Base):
    ## This marks the class as abstract and prevents it from being instantiated
    __abstract__ = True

    __table_args__ = (sa.UniqueConstraint("countryCode", name="_country_code_uc"),)

    id: so.Mapped[sqlalchemy_utils.custom_types.INT_PK]
    commonName: so.Mapped[str | None] = so.mapped_column(sa.String, nullable=True)
    officialName: so.Mapped[str | None] = so.mapped_column(sa.String, nullable=True)
    countryCode: so.Mapped[str | None] = so.mapped_column(sa.String, nullable=False)
    region: so.Mapped[str | None] = so.mapped_column(sa.String, nullable=True)


class NagerCountryModel(NagerCountryModelBase):
    __tablename__ = "country"

    id: so.Mapped[sqlalchemy_utils.custom_types.INT_PK]
    country_id = so.mapped_column(sa.Integer, sa.ForeignKey("country.id"))
    borders = so.relationship("NagerCountryModel")


# class NagerBorderCountryModel(NagerCountryModelBase):
#     __tablename__ = "border_country_info"

#     id: so.Mapped[sqlalchemy_utils.custom_types.INT_PK]


class NagerCountryRepositoryBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, entity: NagerCountryModel) -> None:
        """Add new entity to repository."""
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: NagerCountryModel) -> None:
        """Remove existing entity from repository."""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, country_id: int) -> NagerCountryModel | None:
        """Retrieve entity from repository by its ID."""
        raise NotImplementedError()

    # @abc.abstractmethod
    # def list(self) -> list[NagerCountryModel]:
    #     """List all entities in the repository."""
    #     raise NotImplementedError()
