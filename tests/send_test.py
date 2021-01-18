import random
import socket
import time
import sys

sys.path.append('../core')


import general_utils as gu

ip = 'localhost'
port = 9090

sock = socket.socket(socket.AF_INET,
                    socket.SOCK_DGRAM)

while True:
    msg = str(random.randint(0, 100)).encode()
    sock.sendto(msg, (ip, port))

    time.sleep(3)
