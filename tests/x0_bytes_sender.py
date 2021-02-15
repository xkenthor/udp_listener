import random
import struct
import socket
import time
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

def decode_msg(msg,
            records_per_package=_records_per_package,
            byteorder=_byteorder,
            signed=_signed):
    """
    This function decodes raw bytes message.

    Keyword arguments:
    msg -- < bytes > raw bytes message.
    records_per_package -- < int > number of records message includes.
    byteorder -- < str > -- big/little.
    signed -- < bool > -- True/False.

    Return:
    < list > -- list of decoded records.

    """
    result_list = []

    for record_num in range(records_per_package):
        r_pos = record_num*_template_record_bsize
        record_slice = msg[r_pos:r_pos+_template_record_bsize]

        record_list = []
        b_pos = 0

        for bsize in _template_record_bsize_tuple:
            value = record_slice[b_pos:b_pos+bsize]
            value = int.from_bytes(value, byteorder=byteorder, signed=signed)
            record_list.append(value)
            b_pos += bsize

        result_list.append(record_list)

    return result_list

def cvt_bytes(number, bsize, byteorder=_byteorder, signed=_signed):
    return number.to_bytes(bsize, byteorder=byteorder, signed=signed)

def msg_generator(package_number):
    msg_bytes = b''

    for m_num in range(_measurements_per_package):
        msg_bytes += cvt_bytes(m_num, 4)
        msg_bytes += cvt_bytes(package_number, 4)

        for i in range(_m_range):
            msg_bytes += cvt_bytes(random.randint(_lower, _upper), 2)

    return msg_bytes

msg = msg_generator(0)
print(msg)
print(sys.getsizeof(msg))

print()
print(decode_msg(msg))

#ip = 'localhost'
#port = 9090
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#timer = 1
#
#for i in range(0,-1000000,-1):
#    value = i/10
#    try:
#        3print(value, value.to_bytes(2, byteorder='big', signed=True))
#    except Exception as error:
#        print(error.__str__())
#        input()


# while True:
#     msg = ""
#     for i in range(random.randint(1,5)):
#         msg += (str(random.randint(0, 100))+"&")
#
#     msg = msg[:-1]
#     msg = msg.encode()
#
#     sock.sendto(msg, (ip, port))
#
#     time.sleep(timer)
