import sys

import matplotlib.pyplot as plt

sys.path.append('../core')

import general_utils as gu

save_path = "../gui/dumps/graph_3/1970-01-01_01-01-55_239"

graph = gu.read_gzip(save_path)

print(gu.json.dumps(graph, indent=3))

plt.plot(graph['x'], graph['y'])
plt.show()

