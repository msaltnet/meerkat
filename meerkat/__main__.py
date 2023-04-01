"""meerkat 모듈의 시작
Example)
python -m meerkat
"""
import argparse
from argparse import RawTextHelpFormatter
import sys

if __name__ == "__main__":
    DEFAULT_MODE = 6
    parser = argparse.ArgumentParser(
        description="""Monitoring and Reporting Meerkat""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.print_help()
