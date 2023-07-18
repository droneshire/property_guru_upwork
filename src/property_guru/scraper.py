import json

from bs4 import BeautifulSoup
from lxml import etree

from property_guru.data_types import SearchParams
from property_guru.urls import CreateSearch, PropertyForSale
from util import log
from util.web2_client import Web2Client


class PropertyGuru:
    def __init__(self, dry_run: bool = False) -> None:
        self.web2 = Web2Client()
        self.dry_run = dry_run

    def check_properties(self, parameters: SearchParams) -> None:
        if not parameters:
            log.print_fail("No parameters provided!")
            return

        # response = self.web2.get_request(
        #     url=PropertyForSale.URL,
        #     params=dict(parameters),
        # )

        # if not response:
        #     log.print_fail("Failed to get response!")
        #     return

        with open("/tmp/property_guru.html", "r", encoding="utf-8") as infile:
            data = infile.read()
        soup = BeautifulSoup(data, "html.parser")
        dom = etree.HTML(str(soup))
        listings_xml = dom.xpath('//*[@id="listings-container"]')[0]
        with open("/tmp/property_guru_section.html", "w", encoding="utf-8") as outfile:
            outfile.write(etree.tostring(listings_xml, encoding="unicode"))
        print(len(listings_xml))
        # print([etree.tostring(listings_xml[i], encoding="unicode") for i in range(len(listings_xml))])
