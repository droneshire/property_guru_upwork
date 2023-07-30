import argparse
import os
import typing as T

import dotenv

from bot import ScraperBot
from property_guru.data_types import PROJECT_NAME
from util import log, telegram_util, wait


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Property Guru Bot")

    log_dir = log.get_logging_dir(PROJECT_NAME)

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

    parser.add_argument(
        "--time-between-loops",
        type=int,
        help="Time between each loop (in seconds)",
        default=60,
    )

    src_dir = os.path.dirname(os.path.dirname(__file__))
    root_dir = os.path.dirname(src_dir)
    parser.add_argument(
        "--params-file",
        type=str,
        help="File to store search parameters",
        default=os.path.join(root_dir, "params.json"),
    )

    parser.add_argument(
        "--param-update-period",
        type=int,
        help="Time between each parameter update (in seconds)",
        default=60 * 1,
    )
    parser.add_argument(
        "--firebase-credentials-file",
        type=str,
        help="Firebase credentials file",
        default=os.path.join(root_dir, "firebase_service_account.json"),
    )

    return parser.parse_args()


def setup_telegram(dry_run: bool) -> T.Tuple[telegram_util.TelegramUtil, str]:
    telegram_api_token = os.environ.get("TELEGRAM_API_TOKEN", "")
    telegram_channel_name = os.environ.get("TELEGRAM_BOT_CHANNEL", "")

    telegram = telegram_util.TelegramUtil(telegram_api_token, dry_run=dry_run)

    is_valid = telegram.check_token()

    if not is_valid:
        raise Exception("Telegram token is invalid!")  # pylint: disable=broad-exception-raised

    chat_id = telegram.get_chat_id(telegram_channel_name)

    if chat_id or dry_run:
        log.print_bold(f"Telegram channel id: {chat_id}")
    else:
        log.print_fail(f"Telegram channel {telegram_channel_name} not found!")
        raise Exception("Telegram channel not found!")  # pylint: disable=broad-exception-raised

    return telegram, telegram_channel_name


def run_loop(args: argparse.Namespace) -> None:
    telegram, telegram_channel_name = setup_telegram(args.dry_run)

    bot = ScraperBot(
        telegram,
        telegram_channel_name,
        args.params_file,
        args.firebase_credentials_file,
        args.param_update_period,
        args.dry_run,
    )

    bot.init()

    while True:
        bot.run()
        wait.wait(args.time_between_loops)


def main() -> None:
    args = parse_args()
    dotenv.load_dotenv(".env")

    log.setup_log(args.log_level, args.log_dir, PROJECT_NAME)
    log.print_ok_blue("Starting Property Guru Bot")

    bot_pidfile = os.environ.get("BOT_PIDFILE", "monitor_inventory.pid")

    with open(bot_pidfile, "w", encoding="utf-8") as outfile:
        outfile.write(str(os.getpid()))

    try:
        run_loop(args)
    finally:
        os.remove(bot_pidfile)


if __name__ == "__main__":
    main()
