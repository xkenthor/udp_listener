import random
import struct
import socket
import time

_v_range = 8
_upper = 128
_lower = -127

def msg_generator(package_number, upper, lower):
    values_list = [random.randint(upper, lower) for _ in range(_v_range)]
    pass


ip = 'localhost'
port = 9090
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
timer = 1

for i in range(0,-1000000,-1):
    value = i/10
    try:
        print(value, value.to_bytes(2, byteorder='big', signed=True))
    except Exception as error:
        print(error.__str__())
        input()


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
