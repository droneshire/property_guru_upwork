import typing as T

from property_guru.data_types import ListingSearchParams, PropertyListing
from property_guru.headers import PROPERTY_GURU_API_HEADERS


class ApiCall:
    URL = ""
    RESPONSE_TYPE = T.TypedDict


class PropertyForSale(ApiCall):
    URL = "https://www.propertyguru.com.sg/property-for-sale"


class ListingsApi(ApiCall):
    URL = "https://www.propertyguru.com.sg/api/consumer/listings/other"
    RESPONSE_TYPE = PropertyListing
