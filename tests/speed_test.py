import os
import sys
import time
import random
random.seed(1)

sys.path.append('../core')
import general_utils as gu

def read_gzip():
    plot_dir = "../gui/dumps/graph_0"
    plot_path = os.path.join(plot_dir, os.listdir(plot_dir)[0])

    plot_object = gu.read_gzip(plot_path)
    return plot_object


if __name__ == "__main__":
    plot_object = read_gzip()
    thresh_count = 150000

    for i in range(100):
        for i in range(5):
            start_time = time.time()

            x_length = len(plot_object['x'])

            if len(plot_object['y']) > 150000:
                difference = x_length - thresh_count
                x = plot_object['x']
                y = plot_object['y']

#                plot_object['x'] = plot_object['x'][difference:]
#                plot_object['y'] = plot_object['y'][difference:]

            print('\tEval: {}s.'.format(round(time.time()-start_time, 4)))

            for i in range(random.randint(40, 1000)):
                plot_object['x'].append(random.randint(0, 1000) / 1000)
                plot_object['y'].append(random.randint(0, 1000) / 1000)

        print('')
