from __future__ import annotations

from .__enum import EndpointEnum

AVAILABLE_COUNTRIES: str = EndpointEnum.AVAILABLE_COUNTRIES.value
COUNTRY_INFO: str = EndpointEnum.COUNTRY_INFO.value
LONG_WEEKEND: str = EndpointEnum.LONG_WEEKEND.value
PUBLIC_HOLIDAYS: str = EndpointEnum.PUBLIC_HOLIDAYS.value
IS_TODAY_PUBLIC_HOLIDAY: str = EndpointEnum.IS_TODAY_PUBLIC_HOLIDAY.value
NEXT_PUBLIC_HOLIDAYS: str = EndpointEnum.NEXT_PUBLC_HOLIDAYS.value
NEXT_PUBLIC_HOLIDAYS_WORLD: str = EndpointEnum.NEW_PUBLIC_HOLIDAYS_WORLD.value
API_VERSION: str = EndpointEnum.API_VERSION.value
