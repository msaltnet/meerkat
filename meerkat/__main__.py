"""meerkat 모듈의 시작
Example)
python -m meerkat
"""

import argparse
from argparse import RawTextHelpFormatter
from .telegram_controller import TelegramController

if __name__ == "__main__":
    DEFAULT_MODE = 6
    parser = argparse.ArgumentParser(
        description="""Monitoring and Reporting Meerkat""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("--interval", help="trading tick interval (seconds)", type=int, default="10")

    args = parser.parse_args()
    tcb = TelegramController(interval=args.interval)
    tcb.main()
