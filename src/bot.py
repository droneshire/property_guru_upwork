import copy
import json
import os
import time
import typing as T

from firebase.data_types import User
from firebase.user import FirebaseUser
from property_guru.data_types import SEARCH_PARAMS_DEFAULT, SearchParams
from property_guru.scraper import PropertyGuru
from util import log
from util.format import get_pretty_seconds
from util.telegram_util import TelegramUtil


class ScraperBot:
    TIME_BETWEEN_FIREBASE_QUERIES = {
        "prod": 60 * 15,
        "test": 60,
    }

    def __init__(
        self,
        telegram_util: TelegramUtil,
        params_file: str,
        credentials_file: str,
        param_update_period: int = 60 * 30,
        dry_run: bool = False,
        verbose: bool = False,
    ) -> None:
        self.telegram: TelegramUtil = telegram_util
        self.dry_run = dry_run
        self.scraper = PropertyGuru(dry_run=dry_run)
        self.params_file = params_file
        self.params: T.Dict[str, SearchParams] = {}
        self.param_update_period = param_update_period

        self.firebase_user: FirebaseUser = FirebaseUser(credentials_file, verbose)
        self.last_query_firebase_time: T.Optional[float] = None

        self.mode = "prod" if not dry_run else "test"

    def init(self) -> None:
        self.check_and_update_params()

    def check_and_update_params(self) -> None:
        self._try_to_load_params_from_file()
        self._try_to_update_params_from_firebase()

    def run(self) -> None:
        self.firebase_user.health_ping()
        self._check_firebase()
        for user, params in self.params.items():
            log.print_ok_blue(f"Checking properties for {user}...")
            self.scraper.check_properties(params)

    def _try_to_load_params_from_file(self) -> None:
        if not os.path.exists(self.params_file):
            return

        with open(self.params_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)

        is_valid_data = False
        if isinstance(data, dict):
            for key in SEARCH_PARAMS_DEFAULT:
                if key not in data:
                    break
            is_valid_data = True

        if not is_valid_data:
            log.print_fail("Invalid data in params.json!")
        else:
            self.params["from_file"] = data
            log.print_normal(f"Updated params:\n{json.dumps(self.params, indent=4)}")

    def _try_to_update_params_from_firebase(self) -> None:
        for user, info in self.firebase_user.get_users().items():
            search_params: SearchParams = {
                "minprice": info["searchParams"]["minPrice"],
                "maxprice": info["searchParams"]["maxPrice"],
                "beds": list(
                    range(info["searchParams"]["minBeds"], info["searchParams"]["maxBeds"] + 1)
                ),
                "baths": list(
                    range(info["searchParams"]["minBaths"], info["searchParams"]["maxBaths"] + 1)
                ),
                "minsize": info["searchParams"]["minSize"],
                "maxsize": info["searchParams"]["maxSize"],
                "newProject": "all",
                "search": True,
                "listing_type": "sale",
                "market": "residential",
            }

            self.params[user] = search_params

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
