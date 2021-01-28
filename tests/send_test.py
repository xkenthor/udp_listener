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
# for i in range(100):
    msg = ""
    for i in range(random.randint(1,5)):
        msg += (str(random.randint(0, 100))+"&")

    msg = msg[:-1]
    msg = msg.encode()

    sock.sendto(msg, (ip, port))

    time.sleep(1)
