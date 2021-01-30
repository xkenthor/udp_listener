import threading
import random
import socket
import time
import json
import sys

sys.path.append('../core')

import general_utils as gu
import plot_db as pdb
import port_listener as pl

def generate_msg(value_list, symbol='&'):
    msg = ""
    for value in value_list:
        msg += (str(value)+symbol)

    return msg[:-1]

def port_aggregate(ip, port, gamount, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        value_list = []
        for _ in range(gamount):
            value_list.append(random.randint(-10, 10))
        msg = generate_msg(value_list)
        msg = msg.encode()

        sock.sendto(msg, (ip, port))
        time.sleep(timeout)

# self.dump_plot_object()
# Проверить:
#   __start_processing
#   __start_processing
#   stop_updating
#   start_processing_thread
#   start_processing
#
#   concatenate_2dplot_dot
#   concatenate_2dplot_dot_list

ip = 'localhost'
port = 9090
graphs_amount = 10
timeout = 1


pa_1_t = threading.Thread(target=port_aggregate,
                        name='port_aggregate',
                        args=(ip, port, graphs_amount, timeout))
pa_1_t.start()

pl_1 = pl.UDPServer(ip, port)
pdb_1 = pdb.PlotDB(pl_1, graphs_amount)
pdb_1.set_plot_backup(15)
pdb_1.set_plot_thresh(15)

pdb_1.start_processing_thread()

while True:
    graph_list = gu.log('\n'+json.dumps(pdb_1.get_graph_list(), indent=3))

    time.sleep(1)

pa_1_t.join()
gu.log('All threads has been joined.')
