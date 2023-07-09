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
}
