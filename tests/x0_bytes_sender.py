#!/usr/bin/python
import random
import struct
import socket
import time
import math
import sys

_m_range = 8
_upper = 32767
_lower = -32768
_measurements_per_package = 40

_records_per_package = _measurements_per_package
_template_record_bsize_tuple = (4,4,2,2,2,2,2,2,2,2)
_template_record_bsize = 24

_byteorder = 'little'
_signed = True

def cvt_bytes(number, bsize, byteorder=_byteorder, signed=_signed):
    return number.to_bytes(bsize, byteorder=byteorder, signed=signed)

def msg_generator(package_number, mode=0):
    msg_bytes = b''

    for m_num in range(_measurements_per_package):
        msg_bytes += cvt_bytes(m_num, 4)
        msg_bytes += cvt_bytes(package_number+m_num, 4)

        for i in range(_m_range):
            if mode == 0:
                msg_bytes += cvt_bytes(random.randint(_lower, _upper), 2)
            elif mode == 1:
                msg_bytes += cvt_bytes(int(math.sin(m_num)*100), 2)
            elif mode == 2:
                msg_bytes += cvt_bytes(0, 2)

    return msg_bytes


if __name__ == '__main__':

    ip = 'localhost'
    port = 9090
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timer = 0.1

    pkg_number = 0
    mode = 0
    while True:
        if pkg_number % 1000 == 0:
            mode += 1

            if mode > 2:
                mode = 0

        msg = msg_generator(pkg_number, mode)
        pkg_number += 40

        sock.sendto(msg, (ip, port))
        time.sleep(timer)
