import copy
import json
import os
import random
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
from util import file_util, log
from util.format import get_pretty_seconds
from util.wait import wait
from util.web2_client import Web2Client

DIVIDER_STRING = f"{'=' * 100}"


class PropertyGuru:
    USE_TEST_PARAMS = False
    USE_TEST_HTML = False
    RAW_HTML_LOG_DIR_NAME = os.path.join(log.get_logging_dir(PROJECT_NAME), "search_results")
    WAIT_RANGE = (60, 80)

    def __init__(self, max_pages: int, dry_run: bool = False, verbose: bool = False) -> None:
        self.dry_run = dry_run
        self.verbose = verbose
        self.throttling_time = 0.0
        self.max_pages = max_pages

    def get_properties(self, user: str, parameters: SearchParams) -> T.List[ListingDescription]:
        # pylint: disable=too-many-locals
        if not parameters:
            log.print_fail("No parameters provided!")
            return []

        if self.USE_TEST_PARAMS:
            log.print_ok_blue("Using test params...")
            parameters = copy.deepcopy(TEST_PARAMS)

        if not parameters["property_id"] and not parameters["freetext"]:
            log.print_warn(f"Invalid listing id for {user}, skipping...")
            return []

        request_parameters = {key: value for key, value in parameters.items() if value}

        del request_parameters["property_type"]

        wait_time = random.randint(*self.WAIT_RANGE)
        wait(wait_time)

        log.print_normal(DIVIDER_STRING)

        log.print_bright("PAGE 1")
        log.print_ok_blue(
            f"After waiting for {get_pretty_seconds(int(wait_time))}, checking page 1..."
        )

        browser_url_params = urllib.parse.urlencode(request_parameters)
        browser_url = f"{PropertyForSale.URL}?{browser_url_params}"
        log.print_normal(f"Equivalent search:\n{browser_url}")

        log_dir = os.path.join(PropertyGuru.RAW_HTML_LOG_DIR_NAME, user)
        file_util.make_sure_path_exists(log_dir, ignore_extension=True)

        serialized_params = "-".join(
            [f"{key}={value}" for key, value in request_parameters.items()]
        )
        store_response_html = os.path.join(
            log_dir,
            f"{PropertyForSale.URL.rsplit('/', maxsplit=1)[-1]}-{serialized_params}-page-1.html",
        )

        if self.USE_TEST_HTML and os.path.isfile(store_response_html):
            with open(store_response_html, "r", encoding="utf-8") as infile:
                content = infile.read()
        else:
            log.print_normal(f"Search Params:\n{json.dumps(request_parameters, indent=4)}")
            response = Web2Client(dry_run=self.dry_run).get_request(
                url=PropertyForSale.URL,
                params=request_parameters,
            )

            if not response:
                log.print_fail("Failed to get response!")
                raise ValueError("Failed to get response!")

            with open(store_response_html, "w", encoding="utf-8") as outfile:
                outfile.write(response.content.decode("utf-8"))
            content = response.content

        soup = BeautifulSoup(content, "html.parser")
        properties: T.List[ListingDescription] = []

        pages = self._get_total_pages(soup)

        if pages <= 0:
            log.print_fail("No pages to scrape!")
            return []

        if pages > self.max_pages:
            log.print_warn(f"Found {pages} pages, but only scraping {self.max_pages}...")
            pages = self.max_pages

        properties.extend(self._get_property_info_from_page(soup))

        log.print_ok_arrow(f"Found {len(properties)} properties on page 1/{pages}...")

        log.print_normal(DIVIDER_STRING)

        properties.extend(
            self._get_properties_from_other_pages(
                request_parameters, browser_url_params, log_dir, pages
            )
        )

        return properties

    def _get_properties_from_other_pages(
        self,
        request_parameters: T.Dict[str, T.Any],
        browser_url_params: str,
        log_dir: str,
        pages: int,
    ) -> T.List[ListingDescription]:
        properties = []

        pages_parsed = 1

        for page in range(2, pages + 1):
            pages_parsed += 1
            try:
                new_properties = self._get_property_from_page(
                    page, request_parameters, browser_url_params, log_dir, pages, pages_parsed
                )
                log.print_ok_arrow(f"Found {len(new_properties)} properties on page {page}...")
                properties.extend(new_properties)
                self.throttling_time = 0.0
            except ValueError:
                self.throttling_time = self.throttling_time * 2 + 30
                log.print_fail(
                    f"Failed to get properties on page {page}!\n"
                    f"Throttling {self.throttling_time}s before trying next page..."
                )
                wait(self.throttling_time)
            log.print_normal(DIVIDER_STRING)

        log.print_ok_arrow(f"Found {len(properties)} properties")

        return properties

    def _get_property_from_page(
        self,
        page: int,
        parameters: T.Dict[str, T.Any],
        browser_url_params: str,
        log_dir: str,
        total_pages: int,
        pages_parsed: int,
    ) -> T.List[ListingDescription]:
        if page == 1:
            return []

        url = PropertyForSale.URL + f"/{page}"

        wait_time = random.randint(*self.WAIT_RANGE)
        wait(wait_time)

        log.print_bright(f"PAGE {pages_parsed}/{total_pages}")
        log.print_ok_blue(
            f"After waiting for {get_pretty_seconds(int(wait_time))}, checking page {page}..."
        )

        browser_url = f"{url}?{browser_url_params}"
        log.print_normal(f"Equivalent search:\n{browser_url}")

        response = Web2Client(dry_run=self.dry_run).get_request(
            url=url,
            params=parameters,
        )

        if not response:
            log.print_fail(f"Failed to get response on page {page}!")
            raise ValueError("Failed to get response!")

        store_response_html = os.path.join(
            log_dir,
            (
                f"{PropertyForSale.URL.rsplit('/', maxsplit=1)[-1]}-"
                f"{browser_url_params}-page-{page}.html"
            ),
        )
        with open(store_response_html, "w", encoding="utf-8") as outfile:
            outfile.write(response.content.decode("utf-8"))

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
