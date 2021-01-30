import random
import time
import sys
import os

from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import listener_gshell

def test_plot(plot_widget):
    hour = list(range(150))
    temperature = [random.randint(-1000, 1000) for i in range(150)]
    plot_widget.plot(hour, temperature)


def main():
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = listener_gshell.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # setup_ui(MainWindow)
    w_plot_list = [
        ui.pt_1,
        ui.pt_2,
        ui.pt_3,
        ui.pt_4,
        ui.pt_5,
        ui.pt_6,
    ]
    for plot_widget in w_plot_list:
        test_plot(plot_widget)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
