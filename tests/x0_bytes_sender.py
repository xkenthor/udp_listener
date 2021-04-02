import numpy as np

import random
import socket
import math
import time
import sys

sys.path.append("../core")
import general_utils as gu

_timer = 0.2
_mode_period = 160
_modes_count = 2

_defaults_path = "../settings/defaults.json"
_dft_path = "../settings/data_format_template.json"

_defaults = gu.read_json(_defaults_path)
_dft = gu.read_json(_dft_path)

# data format variables

_rpr = _dft["records_per_package"]
_rbst = _dft["template_record_bsize_tuple"]
_bor = _dft["byteorder"]
_mpp = len(_rbst)

_rbs = 0
for record in _rbst:
    _rbs += record[0]

# general functions

def cvt_bytes(integer, bsize, signed, byteorder=_bor):
    return integer.to_bytes(bsize, byteorder=byteorder, signed=signed)

def sin_wave(integer, div=10, mult=1000):
    integer = math.sin(integer / div) * mult
    return integer

def rand_wave(lower=-32768, upper=32767):
    return random.randint(lower, upper)

def msg_gen(package_number):
    msg_bytes = b''

    for meas_num in range(_rpr):
        msg_bytes += cvt_bytes(meas_num,
                            _rbst[0][0],
                            _rbst[0][1])
        msg_bytes += cvt_bytes(package_number+meas_num,
                            _rbst[1][0],
                            _rbst[1][1])

        for i in range(2, _mpp):
            numer = package_number + meas_num

            if i == 2:
                value = sin_wave(numer)

            elif i == 3:
                value_1 = sin_wave(numer)

            elif i >= 5 and i < _mpp-1:
                value = rand_wave()

            else:
                value = 0

            msg_bytes += cvt_bytes(int(value), _rbst[i][0], _rbst[i][1])

    return msg_bytes


if __name__ == "__main__":

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = _defaults["ip"]
    port = int(_defaults["port"])

    pkg_number = 0

    while True:
        msg = msg_gen(pkg_number)
        pkg_number += 40
        sock.sendto(msg, (ip, port))
        time.sleep(_timer)
