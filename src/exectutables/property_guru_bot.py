import argparse
import os

import dotenv

from util import log


def parse_args():
    parser = argparse.ArgumentParser(description="Property Guru Bot")
    parser.add_argument("--env", type=str, default="dev", help="Environment to run the bot in")
    return parser.parse_args()


def main():
    args = parse_args()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(this_dir)
    dotenv_dir = os.path.dirname(src_dir)

    dotenv.load_dotenv(dotenv_path=os.path.join(dotenv_dir, ".env"))

    log.print_ok_blue("Starting Property Guru Bot")


if __file__ == "__main__":
    main()
