import copy
import json
import os

from property_guru.data_types import SEARCH_PARAMS_DEFAULT, SearchParams
from property_guru.scraper import PropertyGuru
from util import log
from util.telegram_util import TelegramUtil


class ScraperBot:
    def __init__(
        self,
        telegram_util: TelegramUtil,
        params_file: str,
        param_update_period: int = 60 * 30,
        dry_run: bool = False,
    ) -> None:
        self.telegram: TelegramUtil = telegram_util
        self.dry_run = dry_run
        self.scraper = PropertyGuru()
        self.params_file = params_file
        self.params: SearchParams = copy.deepcopy(SEARCH_PARAMS_DEFAULT)
        self.param_update_period = param_update_period

    def init(self) -> None:
        self.check_and_update_params()

    def load_params_from_file(self) -> None:
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
            self.params = data
            log.print_normal(f"Updated params:\n{json.dumps(self.params, indent=4)}")

    def check_and_update_params(self) -> None:
        self.load_params_from_file()

    def scrape_properties(self) -> None:
        self.scraper.check_properties(self.params)

    def run(self) -> None:
        self.scrape_properties()
