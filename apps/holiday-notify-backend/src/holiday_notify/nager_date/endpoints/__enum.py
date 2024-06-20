from enum import Enum


class EndpointEnum(Enum):
    COUNTRY_INFO = "CountryInfo"
    AVAILABLE_COUNTRIES = "AvailableCountries"
    LONG_WEEKEND = "LongWeekend"
    PUBLIC_HOLIDAYS = "PublicHolidays"
    IS_TODAY_PUBLIC_HOLIDAY = "IsTodayPublicHoliday"
    NEXT_PUBLC_HOLIDAYS = "NextPublicHolidays"
    NEW_PUBLIC_HOLIDAYS_WORLD = "NextPublicHolidaysWorldwide"
    API_VERSION = "Version"
