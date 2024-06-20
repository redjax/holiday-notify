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


# borders_association_table = sa.Table(
#     "borders",
#     sqlalchemy_utils.Base.metadata,
#     sa.Column("country_id", sa.Integer, sa.ForeignKey("country.id"), primary_key=True),
#     sa.Column(
#         "border_country_id", sa.Integer, sa.ForeignKey("country.id"), primary_key=True
#     ),
# )


class NagerCountryModel(NagerCountryModelBase):
    __tablename__ = "country"

    id: so.Mapped[sqlalchemy_utils.custom_types.INT_PK]
    country_id = so.mapped_column(sa.Integer, sa.ForeignKey("country.id"))
    borders = so.relationship("NagerCountryModel")


class NagerBorderCountryModel(NagerCountryModelBase):
    __tablename__ = "border_country_info"

    id: so.Mapped[sqlalchemy_utils.custom_types.INT_PK]


# class NagerBorderCountryModel(NagerCountryModelBase):
#     __tablename__ = "borders"

#     # bordering_countries: so.Mapped[list["NagerCountryModel"] | None] = so.relationship(
#     #     "NagerCountryModel",
#     #     secondary=country_border_association,
#     #     primaryjoin="NagerBorderCountryModel.id == country_border_association.c.border_country_id",
#     #     secondaryjoin="NagerCountryModel.id == country_border_association.c.country_id",
#     #     back_populates="borders",
#     # )


# class NagerCountryModel(NagerCountryModelBase):
#     __tablename__ = "countries"

#     # borders: so.Mapped[list[NagerBorderCountryModel] | None] = so.relationship(
#     #     "NagerBorderCountryModel",
#     #     secondary=country_border_association,
#     #     primaryjoin="NagerCountryModel.id == country_border_association.c.country_id",
#     #     secondaryjoin="NagerBorderCountryModel.id == country_border_association.c.border_country_id",
#     #     back_populates="bordering_countries",
#     # )


# # Define the relationships after the models are defined
# NagerBorderCountryModel.bordering_countries = so.relationship(
#     "NagerCountryModel",
#     secondary=country_border_association,
#     primaryjoin="NagerBorderCountryModel.id == country_border_association.c.border_country_id",
#     secondaryjoin="NagerCountryModel.id == country_border_association.c.country_id",
#     back_populates="borders",
# )

# NagerCountryModel.borders = so.relationship(
#     "NagerBorderCountryModel",
#     secondary=country_border_association,
#     primaryjoin="NagerCountryModel.id == country_border_association.c.country_id",
#     secondaryjoin="NagerBorderCountryModel.id == country_border_association.c.border_country_id",
#     back_populates="bordering_countries",
# )


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
