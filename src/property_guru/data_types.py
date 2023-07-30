import typing as T


class SearchParams(T.TypedDict):
    listing_type: str
    market: str
    baths: T.List[int]
    beds: T.List[int]
    maxprice: int
    minprice: int
    maxsize: int
    minsize: int
    newProject: str
    search: bool
    property_id: int


SEARCH_PARAMS_DEFAULT: SearchParams = {
    "listing_type": "sale",
    "market": "residential",
    "baths": [1, 2, 3, 4, 5],
    "beds": [1, 2, 3, 4, 5],
    "maxprice": 3000000,
    "minprice": 0,
    "maxsize": 6000,
    "minsize": 0,
    "newProject": "all",
    "search": True,
    "property_id": 0,
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
    link: dict[str, str]


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
    link: dict[str, str]
    data: PropertyDetails
    pricing: PropertyPricing
    rooms: PropertyRooms


class PropertyListing(T.TypedDict):
    metadata: dict
    context: PropertyContext
    shouldRenderRooms: bool
