import json
import time
import typing as T

from firebase.user import FirebaseUser
from property_guru.data_types import ListingDescription
from property_guru.scraper import PropertyGuru
from property_guru.search import Search
from util import log
from util.format import get_pretty_seconds
from util.telegram_util import TelegramUtil
from util.wait import wait


class ScraperBot:
    TIME_BETWEEN_FIREBASE_QUERIES = {
        "prod": 60 * 30,
        "test": 60,
    }

    def __init__(
        self,
        telegram_util: TelegramUtil,
        telegram_channel_name: str,
        credentials_file: str,
        param_update_period: int = 60 * 30,
        dry_run: bool = False,
        verbose: bool = False,
    ) -> None:
        self.telegram: TelegramUtil = telegram_util
        self.telegram_channel_name = telegram_channel_name
        self.telegram_channel_id = 0
        self.dry_run = dry_run
        self.scraper = PropertyGuru(dry_run=dry_run, verbose=verbose)
        self.param_update_period = param_update_period

        self.searches: T.List[Search] = []
        self.listing_ids: T.Dict[str, T.List[int]] = {}

        self.firebase_user: FirebaseUser = FirebaseUser(credentials_file, verbose)
        self.last_query_firebase_time: T.Optional[float] = None

        self.mode = "prod" if not dry_run else "test"

        self.throttling_time = 0.0

    def init(self) -> None:
        self.check_and_update_params()
        channel_id = self.telegram.get_chat_id(self.telegram_channel_name)
        if channel_id:
            self.telegram_channel_id = channel_id

    def check_and_update_params(self) -> None:
        self._try_to_update_data_from_firebase()

    def run(self) -> None:
        self.firebase_user.health_ping()
        self._check_firebase()

        for query in self.searches:
            log.print_ok_blue(f"Checking properties for {query.user}...")
            try:
                current_listings: T.List[ListingDescription] = self.scraper.get_properties(
                    query.user, query.search
                )
            except ValueError:
                self.throttling_time = self.throttling_time * 2 + 30
                log.print_fail(f"Failed to get properties! Throttling {self.throttling_time}s...")
                wait(self.throttling_time)
                break

            if not current_listings:
                continue

            current_listings_by_id = {
                int(listing["listing_id"]): listing for listing in current_listings
            }

            previous_listings = self.listing_ids.get(query.user, [])
            new_listing_ids = list(set(current_listings_by_id.keys()) - set(previous_listings))

            if not new_listing_ids:
                continue

            log.print_ok(f"Found {len(new_listing_ids)} new listings!")
            self.listing_ids[query.user] = list(current_listings_by_id.keys())
            for listing_id in new_listing_ids:
                listing = current_listings_by_id[listing_id]
                if not self._handle_new_listing(query.user, listing):
                    log.print_warn(f"Failed to send message for {query.user}!")
                    self.listing_ids[query.user].remove(listing_id)

                time.sleep(5.0)

            self.throttling_time = 0.0

        self._try_to_update_data_to_firebase()

    def _handle_new_listing(self, user: str, listing: ListingDescription) -> bool:
        log.print_bold(f"New listing found for {user}!\n\n")
        log.print_normal(json.dumps(listing, indent=4))
        house_emoji = "\U0001f3e0"
        message = f"{house_emoji * 2} New listing found for {user}!\n"
        message += f"Listing ID: {listing['listing_id']}\n"
        message += f"Listing Title: {listing['listing_title']}\n"
        message += f"Listing URL: {listing['listing_url']}\n"
        message += f"Listing Address: {listing['listing_address']}\n"
        message += f"Price: {listing['price']}\n"
        message += f"Beds: {listing['beds']}\n"
        message += f"Baths: {listing['baths']}\n"
        message += f"Square Footage: {listing['square_footage']}\n"

        if not self.telegram_channel_id:
            log.print_fail(f"Telegram channel {self.telegram_channel_name} not found!")
            return False

        try:
            self.telegram.send_message(self.telegram_channel_id, message)
            return True
        except:  # pylint: disable=bare-except
            log.print_fail("Failed to send message!")
            return False

    def _try_to_update_data_to_firebase(self) -> None:
        for user, ids in self.listing_ids.items():
            log.print_bold(f"Updating listing ids for {user} to firebase...")
            self.firebase_user.update_listing_ids(user, ids)

    def _try_to_update_data_from_firebase(self) -> None:
        self.searches = self.firebase_user.get_searches()
        users = set(search.user for search in self.searches)

        for user, _ in self.listing_ids.items():
            if user not in users:
                log.print_warn(f"Found user {user} w/out params. Removing cached params")
                del self.listing_ids[user]

    def _check_firebase(self) -> None:
        update_from_firebase = False
        if self.last_query_firebase_time is None:
            update_from_firebase = True
        else:
            time_since_last_update = time.time() - self.last_query_firebase_time
            update_from_firebase = (
                time_since_last_update > self.TIME_BETWEEN_FIREBASE_QUERIES[self.mode]
            )

        if update_from_firebase:
            self.last_query_firebase_time = time.time()
            self.firebase_user.update_watchers()
        else:
            time_till_next_update = int(
                self.TIME_BETWEEN_FIREBASE_QUERIES[self.mode] - time_since_last_update
            )
            log.print_normal(
                f"Next firebase manual refresh in {get_pretty_seconds(time_till_next_update)}"
            )

        self.firebase_user.check_and_maybe_handle_firebase_db_updates()
        self._try_to_update_data_from_firebase()
