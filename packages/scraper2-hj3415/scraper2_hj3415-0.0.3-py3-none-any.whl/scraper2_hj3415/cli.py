from .nfscrapy import run
from krx_hj3415 import krx
import argparse


def c101_one(code: str):
    run.c101([code, ], "mongodb://192.168.0.173:27017")


def c101_all():
    run.c101(krx.get_codes(), "mongodb://192.168.0.173:27017")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--code', action="store", help='code')
    args = parser.parse_args()

    c101_one(args.code)


if __name__ == '__main__':
    main()