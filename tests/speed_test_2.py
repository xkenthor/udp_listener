import copy
import time
import random
random.seed(1)

import speed_test as sp

plot_object = sp.read_gzip()
plot_object_2 = copy.deepcopy(plot_object)

thresh_count = 150000

atime = 0
ctime = 0

for i in range(100):
    for i in range(5):
        start_time = time.time()
        x_length = len(plot_object['x'])

        if len(plot_object['y']) > thresh_count:
            difference = x_length - thresh_count

#            plot_object['x'] = plot_object['x'][difference:]
#            plot_object['y'] = plot_object['y'][difference:]
            del plot_object['x'][:difference]
            del plot_object['y'][:difference]

        e_time = time.time() - start_time
        atime += e_time
        ctime += 1
        print("Eval: {}s. {}".format(round(e_time, 4), x_length))

        for i in range(random.randint(40, 1000)):
            plot_object['x'].append(random.randint(0, 1000) / 1000)
            plot_object['y'].append(random.randint(0, 1000) / 1000)

    print('')

print('\nMean value: {}s.'.format(round(atime/ctime, 4)))
