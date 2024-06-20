import logging

log = logging.getLogger("holiday_notify.domain.NagerDate.schemas")

import typing as t
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ValidationError,
    ConfigDict,
    computed_field,
)


class NagerCountryMeta(BaseModel):
    name: str = Field(default=None)
    countryCode: str = Field(default=None)


class ListNagerCountryMetas(BaseModel):
    countries: list[NagerCountryMeta] = Field(default=None)

    @computed_field
    @property
    def count(self) -> int:
        if (
            self.countries is None
            or isinstance(self.countries, list)
            and len(self.countries) == 0
        ):
            return 0
        else:
            return len(self.countries)


class NagerCountryBase(BaseModel):
    commonName: str = Field(default=None)
    officialName: str = Field(default=None)
    countryCode: str = Field(default=None)
    region: str = Field(default=None)


class NagerBorderCountry(NagerCountryBase):
    pass


class NagerCountry(NagerCountryBase):

    borders: list[NagerBorderCountry] = Field(default=None)
