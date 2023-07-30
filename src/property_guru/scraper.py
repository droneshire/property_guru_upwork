import copy
import json
import os
import random
import time
import typing as T
import urllib

from bs4 import BeautifulSoup
from lxml import etree

from property_guru.data_types import ListingDescription, SearchParams, TEST_PARAMS
from property_guru.urls import PropertyForSale
from util import log
from util.web2_client import Web2Client


class PropertyGuru:
    USE_TEST_PARAMS = True

    def __init__(self, dry_run: bool = False) -> None:
        self.web2 = Web2Client(dry_run=dry_run)
        self.dry_run = dry_run

    def _get_xpath(self, element: BeautifulSoup) -> str:
        xpath = ""
        for parent in element.parents:
            if parent.name:
                siblings = parent.find_all(parent.name, recursive=False)
                try:
                    xpath_index = siblings.index(element) + 1
                except ValueError:
                    # If the element is not found in the parent's siblings,
                    # skip it or handle it differently.
                    continue
                xpath = f"/{parent.name}[{xpath_index}]{xpath}"
            element = parent
        return f"/{element.name}{xpath}"

    def check_properties(self, parameters: SearchParams) -> None:
        if not parameters:
            log.print_fail("No parameters provided!")
            return

        if self.USE_TEST_PARAMS:
            log.print_ok_blue("Using test params...")
            parameters = copy.deepcopy(TEST_PARAMS)

        browser_url_params = urllib.parse.urlencode(parameters)
        browser_url = f"{PropertyForSale.URL}?{browser_url_params}"
        log.print_normal(f"Equivalent search:\n{browser_url}")

        response = self.web2.get_request(
            url=PropertyForSale.URL,
            params=dict(parameters),
        )

        if not response:
            log.print_fail("Failed to get response!")
            return

        store_response_html = os.path.join(
            log.get_logging_dir("property_guru_bot"), f"{PropertyForSale.URL}.html"
        )
        with open(store_response_html, "w") as outfile:
            outfile.write(response.content.decode("utf-8"))

        soup = BeautifulSoup(response.content, "html.parser")
        properties = []

        pages = self.get_total_pages(soup)

        properties.extend(self.get_property_info_from_page(soup))

        # iterate through random pages but make sure we get them all
        for page in random.sample(range(1, pages + 1), pages):
            log.print_ok_blue(f"Checking page {page}...")

            if page == 1:
                continue

            url = PropertyForSale.URL + f"/{page}"

            time.sleep(random.randint(20, 60))

            browser_url = f"{url}?{browser_url_params}"
            log.print_normal(f"Equivalent search:\n{browser_url}")

            response = self.web2.get_request(
                url=url,
                params=dict(parameters),
            )

            if not response:
                log.print_fail("Failed to get response on page {page}!")
                continue

            soup = BeautifulSoup(response.content, "html.parser")

            properties.extend(self.get_property_info_from_page(soup))

    def get_property_info_from_page(self, soup: BeautifulSoup) -> T.List[T.Dict[str, str]]:
        listings_elements = soup.find_all("div", class_="col-xs-12 col-sm-7 listing-description")
        listings_elements.extend(
            soup.find_all("div", class_="col-xs-12 col-sm-12 listing-description")
        )

        properties = []
        for listing_element in listings_elements:
            listing = self.parse_listing_description(listing_element)
            properties.append(listing)
            log.print_normal(f"Found property: {json.dumps(listing, indent=4)}")

        return properties

    def get_total_pages(self, soup: BeautifulSoup) -> int:
        pagination_element = soup.find("ul", class_="pagination")

        if not pagination_element:
            log.print_bright(f"Found 1 page to scrape...")
            return 1

        links = pagination_element.find_all("a", href=True)
        max_page = 0

        for link in links:
            page_number = int(link["data-page"])
            max_page = max(max_page, page_number)

        log.print_bright(f"Found {max_page} pages to scrape...")

        return max_page

    def parse_listing_description(self, description_element: BeautifulSoup) -> ListingDescription:
        listing_title_element = description_element.find("h3", class_="ellipsis")
        listing_title = listing_title_element.text.strip()
        listing_url = listing_title_element.a["href"]

        # Extract listing address
        listing_address_element = description_element.find("span", itemprop="streetAddress")
        listing_address = listing_address_element.text.strip()

        # Extract price
        price_element = description_element.find("span", class_="price")
        price = price_element.text.strip()

        # Extract beds and baths
        beds_element = description_element.find("span", class_="bed")
        beds = beds_element.text.strip()
        baths_element = description_element.find("span", class_="bath")
        baths = baths_element.text.strip()

        # Extract square footage
        square_footage_element = description_element.find(
            "li", class_="listing-floorarea pull-left"
        )
        square_footage = square_footage_element.text.strip()

        # Extract listing ID (from the URL)
        listing_id = listing_url.split("/")[-1].split("-")[-1]

        return ListingDescription(
            {
                "listing_title": listing_title,
                "listing_url": listing_url,
                "listing_address": listing_address,
                "price": price,
                "beds": beds,
                "baths": baths,
                "square_footage": square_footage,
                "listing_id": listing_id,
            }
        )
