import json
import os

from property_guru.data_types import SearchParams
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
        self.params: SearchParams = SearchParams()
        self.param_update_period = param_update_period

    def init(self) -> None:
        self.check_and_update_params()

    def load_params_from_file(self) -> SearchParams:
        if not os.path.exists(self.params_file):
            return {}

        with open(self.params_file, "r", encoding="utf-8") as infile:
            params = json.load(infile)

        return params

    def check_and_update_params(self) -> None:
        params = self.load_params_from_file()
        if params:
            self.params = params
        else:
            log.print_warn("No params.json file found!")

    def scrape_properties(self) -> None:
        self.scraper.check_properties(self.params)

    def run(self) -> None:
        self.scrape_properties()
