import typing as T

PROJECT_NAME = "property_guru_bot"
INVALID_LISTING_ID = -1


class SearchParams(T.TypedDict):
    listing_type: str
    market: str
    baths: str
    beds: str
    maxprice: int
    minprice: int
    maxsize: int
    minsize: int
    newProject: str
    search: bool
    property_id: str
    freetext: str
    sort: str
    order: str
    property_type: str


SEARCH_PARAMS_DEFAULT: SearchParams = {
    "listing_type": "sale",
    "market": "residential",
    "baths": "[1, 2, 3, 4, 5]",
    "beds": "[0, 1, 2, 3, 4, 5]",
    "maxprice": 15000000,
    "minprice": 0,
    "maxsize": 6000,
    "minsize": 0,
    "newProject": "all",
    "search": True,
    "property_id": "0",
    "freetext": "",
    "sort": "date",
    "order": "desc",
    "property_type": "[H, C, L]",
}

TEST_PARAMS: SearchParams = {
    "listing_type": "sale",
    "market": "residential",
    "baths": "[1, 2, 3, 4, 5]",
    "beds": "[0, 1, 2, 3, 4, 5]",
    "maxprice": 15000000,
    "minprice": 0,
    "maxsize": 6000,
    "minsize": 0,
    "newProject": "all",
    "search": True,
    "property_id": "71",
    "freetext": "",
    "sort": "date",
    "order": "desc",
    "property_type": "[H, C, L]",
}


class ListingSearchParams(T.TypedDict):
    projectUrl: str
    statusCode: str
    listingType: str
    bedrooms: str
    baths: str
    listingTypeText: str
    propertyName: str
    locale: str
    region: str


LISTING_SEARCH_PARAMS_DEFAULT: ListingSearchParams = {
    "projectUrl": "",
    "statusCode": "ACT",
    "listingType": "SALE",
    "bedrooms": "",
    "baths": "",
    "listingTypeText": "For Sale",
    "propertyName": "",
    "locale": "en",
    "region": "sg",
}


class PropertyData(T.TypedDict):
    id: int
    title: str
    address: str
    image: str
    link: T.Dict[str, str]


class PropertyDetails(T.TypedDict):
    typeLabel: str


class PropertyPricing(T.TypedDict):
    price: str


class PropertyRooms(T.TypedDict):
    baths: int
    beds: int
    isStudioOrRoom: bool


class PropertyContextData(T.TypedDict):
    id: int
    name: str
    price: int
    category: str
    brand: str
    variant: str
    position: int
    dimension19: int
    dimension22: str
    dimension23: str
    dimension24: str
    dimension25: int
    dimension40: str


class PropertyContext(T.TypedDict):
    data: PropertyContextData


class PropertyInfo(T.TypedDict):
    id: int
    title: str
    address: str
    image: str
    link: T.Dict[str, str]
    data: PropertyDetails
    pricing: PropertyPricing
    rooms: PropertyRooms


class PropertyListing(T.TypedDict):
    metadata: T.Dict[str, str]
    context: PropertyContext
    shouldRenderRooms: bool


class ListingDescription(T.TypedDict):
    listing_title: str
    listing_url: str
    listing_address: str
    price: str
    beds: str
    baths: str
    square_footage: str
    listing_id: int
