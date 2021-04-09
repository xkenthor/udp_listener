from scipy.fft import rfft, rfftfreq, irfft
import numpy as np

import random
import socket
import math
import time
import sys

sys.path.append("../core")
import general_utils as gu
import matplotlib.pyplot as plt

_timer = 0.01
_mode_period = 160
_modes_count = 2

_defaults_path = "../settings/defaults.json"
_dft_path = "../settings/data_format_template.json"

_defaults = gu.read_json(_defaults_path)
_dft = gu.read_json(_dft_path)

_value_array = []

# data format variables

_rpr = _dft["records_per_package"]
_rbst = _dft["template_record_bsize_tuple"]
_bor = _dft["byteorder"]
_td = _dft["time_delay"]
_mpp = len(_rbst)

_rbs = 0
for record in _rbst:
    _rbs += record[0]

def cvt_bytes(integer, bsize, signed, byteorder=_bor):
    return integer.to_bytes(bsize, byteorder=byteorder, signed=signed)

def sin_wave(value, frequency, multiplier=100):
    value = 2 * math.pi * value * frequency
    result = math.sin(math.radians(math.degrees(value)))
    result *= multiplier

    return result

def rand_wave(lower=-32768, upper=32767):
    return random.randint(lower, upper)

_value_array = []
_max_size = 1500

def msg_gen(package_number):
    msg_bytes = b''

    freq_1 = 0.1
    freq_2 = 0.05
    sample_rate = 1 * _td

    for measurement_number in range(_rpr):
        current_number = package_number + measurement_number
        current_time = current_number * _td

        sin_1 = sin_wave(current_time, freq_1)
        sin_2 = sin_wave(current_time, freq_2)
        sin_3 = sin_1 + sin_2
        _value_array.append(sin_3)

        if len(_value_array) > _max_size:
            _value_array.pop(0)

        msg_bytes += cvt_bytes(measurement_number, _rbst[0][0], _rbst[0][1])
        msg_bytes += cvt_bytes(current_number, _rbst[1][0], _rbst[1][1])

        for i in range(2, _mpp):
            if i == 2:
                value = sin_1

            elif i == 3:
                value = sin_2

            elif i == 4:
                value = sin_3

            elif i == 5:
                value = gu.remove_freq_list(_value_array, 1/sample_rate, [freq_1])[-1]

            elif i == 8:
                value = sin_3

            elif i == 9:
                value = sin_3

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
