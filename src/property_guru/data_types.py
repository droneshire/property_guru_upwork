import typing as T


class SearchParams(T.TypedDict):
    listing_type: str
    market: str
    baths: T.List[int]
    beds: T.List[int]
    maxprice: int
    maxsize: int
    minsize: int
    newProject: str
    search: bool
