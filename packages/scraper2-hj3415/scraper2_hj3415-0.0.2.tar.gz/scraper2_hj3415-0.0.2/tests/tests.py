from nfscrapy.run import *
from krx_hj3415 import krx

if __name__ == '__main__':
    c101(krx.get_codes(), "mongodb://192.168.0.173:27017")
