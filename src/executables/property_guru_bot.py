import argparse
import asyncio
import os

import dotenv

from property_guru import scraper
from util import log, telegram_util


def parse_args():
    parser = argparse.ArgumentParser(description="Property Guru Bot")

    log_dir = log.get_logging_dir("property_guru_bot")

    parser.add_argument("--log-dir", default=log_dir)
    parser.add_argument(
        "--log-level",
        type=str,
        help="Logging level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the script without actually sending SMS",
    )

    return parser.parse_args()


async def main():
    args = parse_args()
    dotenv.load_dotenv(".env")

    bot_pidfile = os.environ.get("BOT_PIDFILE", "monitor_inventory.pid")

    with open(bot_pidfile, "w", encoding="utf-8") as outfile:
        outfile.write(str(os.getpid()))

    try:
        log.setup_log(args.log_level, args.log_dir, "prop_guru")

        log.print_ok_blue("Starting Property Guru Bot")

        telegram_api_token = os.environ.get("TELEGRAM_API_TOKEN", "")
        telegram = telegram_util.TelegramUtil(telegram_api_token)

        await telegram.check_token()
        chats = await telegram.get_chats()
        for chat in chats:
            log.print_normal(f"{chat}")
        # await telegram.send_message("@PropertyGuruBot", "Hello World!")

        prop_guru = scraper.PropertyGuru()

        prop_guru.check_properties(
            {"market": "residential", "maxprice": 3000000, "search": True, "listing_type": "sale"}
        )
    finally:
        os.remove(bot_pidfile)


if __name__ == "__main__":
    asyncio.run(main())
