from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import time
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    hour = [1,2,3,4,5,6,7,8,9,10]
    temperature = [30,32,34,32,33,31,29,32,35,45]
    time.sleep(1)
    main.graphWidget.plot(hour, temperature)
    temperature = [32,34,32,33,31,29,32,35,45,56]
    time.sleep(1)
    main.graphWidget.plot(hour, temperature)
    temperature = [34,32,33,31,29,32,35,45,56,34]
    time.sleep(1)
    main.graphWidget.plot(hour, temperature)


    # plot data: x, y values
    main.graphWidget.plot(hour, temperature)a

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
