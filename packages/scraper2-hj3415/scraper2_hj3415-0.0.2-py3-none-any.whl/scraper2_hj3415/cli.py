from nfscrapy import run
from krx_hj3415 import krx


def c101_all():
    run.c101(krx.get_codes(), "mongodb://192.168.0.173:27017")
