import json

from bs4 import BeautifulSoup

from property_guru.data_types import SearchParams
from property_guru.urls import CreateSearch, PropertyForSale
from util import log
from util.web2_client import Web2Client


class PropertyGuru:
    def __init__(self) -> None:
        self.web2 = Web2Client()

    def update_parameters(self, parameters: SearchParams) -> None:
        data = CreateSearch.DATA.format(json.dumps(parameters))
        url = CreateSearch.URL
        response = self.web2.post_request(
            url=url,
            data=data,
        )
        print(response)

    def check_properties(self, parameters: SearchParams) -> None:
        if not parameters:
            log.print_fail("No parameters provided!")
            return

        response = self.web2.get_request(
            url=PropertyForSale.URL,
            params=dict(parameters),
        )
        print(response)
