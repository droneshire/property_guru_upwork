from property_guru.data_types import SearchParams


class Search:
    def __init__(self, user: str, params: SearchParams) -> None:
        self._user = user
        self._search: SearchParams = params

    def __repr__(self) -> str:
        return f"UserSearches(user={self._user}, searches={self._search})"

    @property
    def search(self) -> SearchParams:
        return self._search

    @search.setter
    def search(self, search: SearchParams) -> None:
        self._search = search

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, user: str) -> None:
        self._user = user
