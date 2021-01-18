import threading
import random
import time

import matplotlib.pyplot as plt

# def crop_data(time, data):
#
# def upd_plot():
#
#     udp_s = UDPServer(_default_ip, _default_port)
#     udp_s.serve_forever_thread()
#
#     while True:
#         data = udp_s.get_current_data()
#         data = int(data)

def get_value(value):
    if random.randint(0,10) < 8:
        rint = random.randint(-2,2)
    else:
        rint = random.randint(-10,10)

    value += rint
    return value

arr_1 = [0 for i in range(50)]
arr_2 = [0 for i in range(50)]

step = 0.00001

time_1 = 50
c_value = 50
while True:
    plt.clf()
    plt.title("PLD")
    plt.xlabel('time')
    plt.ylabel('value')
    plt.ylim(0,100)
    plt.grid()

    plt.plot(arr_1, arr_2)
    plt.draw()
    plt.pause(0.0001)
    plt.show(block=False)

    time.sleep(step)
    time_1 += 0.5

    arr_1.pop(0)
    arr_2.pop(0)

    c_value = get_value(c_value)

    arr_1.append(time_1)
    arr_2.append(c_value)
