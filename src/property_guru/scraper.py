import json
import typing as T
import BeautifulSoup
import cloudscraper

from property_guru.data_types import SearchParams
from property_guru.urls import CreateSearch, PropertyForSale
from util import log
from util.web2_client import Web2Client


class PropertyGuru:
    def __init__(self):
        self.w2 = Web2Client()

    def update_parameters(self, parameters: SearchParams) -> None:
        data = CreateSearch.DATA.format(json.dumps(parameters))
        url = CreateSearch.URL
        response = self.w2.post_request(
            url=url,
            headers=header,
            data=data,
        )

    def check_properties(self, parameters: SearchParams) -> None:
        response = self.w2.get_request(
            url=PropertyForSale.URL,
            params=parameters,
        )
        print(response)
