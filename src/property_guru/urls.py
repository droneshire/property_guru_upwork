import typing as T

from property_guru.data_types import PropertyListing


class ApiCall:
    URL = ""
    RESPONSE_TYPE = T.TypedDict


class PropertyForSale(ApiCall):
    URL = "https://www.propertyguru.com.sg/property-for-sale"


class ListingsApi(ApiCall):
    URL = "https://www.propertyguru.com.sg/api/consumer/listings/other"
    RESPONSE_TYPE = PropertyListing
