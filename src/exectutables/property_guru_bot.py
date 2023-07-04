import argparse
import os

import dotenv

from util import log


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


def main():
    args = parse_args()

    dotenv.load_dotenv(".env")

    bot_pidfile = os.environ.get("BOT_PIDFILE", "monitor_inventory.pid")

    with open(bot_pidfile, "w", encoding="utf-8") as outfile:
        outfile.write(str(os.getpid()))

    log.setup_log(args.log_level, args.log_dir, "prop_guru")

    log.print_ok_blue("Starting Property Guru Bot")


if __file__ == "__main__":
    main()
