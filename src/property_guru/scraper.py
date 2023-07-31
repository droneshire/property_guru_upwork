import copy
import json
import os
import random
import time
import typing as T
import urllib

from bs4 import BeautifulSoup
from bs4.element import Tag

from property_guru.data_types import (
    INVALID_LISTING_ID,
    PROJECT_NAME,
    TEST_PARAMS,
    ListingDescription,
    SearchParams,
)
from property_guru.urls import PropertyForSale
from util import log
from util.web2_client import Web2Client


class PropertyGuru:
    USE_TEST_PARAMS = False
    USE_TEST_HTML = False

    def __init__(self, dry_run: bool = False, verbose: bool = False) -> None:
        self.web2 = Web2Client(dry_run=dry_run)
        self.dry_run = dry_run
        self.verbose = verbose

    def get_properties(self, parameters: SearchParams) -> T.List[ListingDescription]:
        if not parameters:
            log.print_fail("No parameters provided!")
            return []

        if self.USE_TEST_PARAMS:
            log.print_ok_blue("Using test params...")
            parameters = copy.deepcopy(TEST_PARAMS)

        browser_url_params = urllib.parse.urlencode(parameters)
        browser_url = f"{PropertyForSale.URL}?{browser_url_params}"
        log.print_normal(f"Equivalent search:\n{browser_url}")

        store_response_html = os.path.join(
            log.get_logging_dir(PROJECT_NAME),
            f"{PropertyForSale.URL.rsplit('/', maxsplit=1)[-1]}.html",
        )

        if self.USE_TEST_HTML and os.path.isfile(store_response_html):
            with open(store_response_html, "r", encoding="utf-8") as infile:
                content = infile.read()
        else:
            response = self.web2.get_request(
                url=PropertyForSale.URL,
                params=dict(parameters),
            )

            if not response:
                log.print_fail("Failed to get response!")
                return []

            with open(store_response_html, "w", encoding="utf-8") as outfile:
                outfile.write(response.content.decode("utf-8"))
            content = response.content

        soup = BeautifulSoup(content, "html.parser")
        properties: T.List[ListingDescription] = []

        pages = self._get_total_pages(soup)

        if pages <= 0:
            log.print_fail("No pages to scrape!")
            return []

        properties.extend(self._get_property_info_from_page(soup))

        # iterate through random pages but make sure we get them all
        for page in random.sample(range(1, pages + 1), pages):
            new_properties = self._get_property_from_page(page, parameters, browser_url_params)
            properties.extend(new_properties)

        log.print_ok_blue_arrow(f"Found {len(properties)} properties")
        return properties

    def _get_xpath(self, element: T.Any) -> str:
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

    def _get_property_from_page(
        self, page: int, parameters: SearchParams, browser_url_params: str
    ) -> T.List[ListingDescription]:
        log.print_ok_blue(f"Checking page {page}...")

        if page == 1:
            return []

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
            return []

        soup = BeautifulSoup(response.content, "html.parser")

        return self._get_property_info_from_page(soup)

    def _get_property_info_from_page(self, soup: Tag) -> T.List[ListingDescription]:
        listings_elements = soup.find_all("div", class_="col-xs-12 col-sm-7 listing-description")
        listings_elements.extend(
            soup.find_all("div", class_="col-xs-12 col-sm-12 listing-description")
        )

        properties = []
        for listing_element in listings_elements:
            listing = self._parse_listing_description(listing_element)
            properties.append(listing)
            if self.verbose:
                log.print_normal(f"Found property: {json.dumps(listing, indent=4)}")

        return properties

    def _get_total_pages(self, soup: Tag) -> int:
        no_results_element = soup.find("span", class_="shorten-search-summary-title")
        no_results_string = no_results_element.text.strip()  # type: ignore

        if "No Results of Property For Sale" in no_results_string:
            log.print_bright("No results found with current params!")
            return 0

        pagination_element = soup.find("ul", class_="pagination")

        if not pagination_element:
            log.print_bright("Found 1 page to scrape...")
            return 1

        links = pagination_element.find_all("a", href=True)  # type: ignore
        max_page = 0

        for link in links:
            page_number = int(link["data-page"])
            max_page = max(max_page, page_number)

        log.print_bright(f"Found {max_page} pages to scrape...")

        return max_page

    def _parse_listing_description(self, description_element: Tag) -> ListingDescription:
        # pylint: disable=too-many-locals
        listing_title_element = description_element.find("h3", class_="ellipsis")
        listing_title = listing_title_element.text.strip()  # type: ignore
        listing_url = listing_title_element.a["href"]  # type: ignore

        # Extract listing address
        listing_address_element = description_element.find("span", itemprop="streetAddress")
        listing_address = listing_address_element.text.strip()  # type: ignore

        # Extract price
        price_element = description_element.find("span", class_="price")
        price = price_element.text.strip()  # type: ignore

        # Extract beds and baths
        beds_element = description_element.find("span", class_="bed")
        beds = beds_element.text.strip()  # type: ignore
        baths_element = description_element.find("span", class_="bath")
        baths = baths_element.text.strip()  # type: ignore

        # Extract square footage
        square_footage_element = description_element.find(
            "li", class_="listing-floorarea pull-left"
        )
        square_footage = square_footage_element.text.strip()  # type: ignore

        # Extract listing ID (from the URL)
        if isinstance(listing_url, list):
            listing_url = "/".join(listing_url)

        if listing_url.endswith("/"):
            listing_url = listing_url[:-1]

        if "?" in listing_url:
            listing_url = listing_url.split("?")[0]

        listing_id = listing_url.split("/")[-1].split("-")[-1]

        if listing_id.isdigit():
            listing_id = int(listing_id)
        else:
            log.print_warn(f"Invalid listing id {listing_id}!")
            listing_id = INVALID_LISTING_ID

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
