"""
This module implements backend logic for graphical shell and connects it with
    core modules.

"""
import random
import time
import sys
import os

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot

import pyqtgraph as pg

import listener_gshell
sys.path.append('../core')
import general_utils as gu
import plot_db as ptdb
import port_listener as ptlr


class ListenerBackEnd():

    def __init__(self, ip, port, dump_save_path):
        """
        This method implements backend logic for graphical shell.

        """
        self.__graph_amount = 6
        self.__port_listener = ptlr.UDPServer(ip, port)
        self.__plot_db = ptdb.PlotDB(self.__port_listener,
                                    self.__graph_amount,
                                    dump_save_path)
        # self.__plot_db.set_plot_thresh(20)

        self.__plot_db.start_processing_thread()

        self.__main_window = QtWidgets.QMainWindow()
        self.__ui = listener_gshell.Ui_MainWindow()

        self.__ui.setupUi(self.__main_window)
        self.__main_window.show()

        self.__plot_tuple = (
            self.__ui.pt_1,
            self.__ui.pt_2,
            self.__ui.pt_3,
            self.__ui.pt_4,
            self.__ui.pt_5,
            self.__ui.pt_6
        )

        self.__init_all_connections()
        self.__init_all_widgets()

        self.__data_list_tuple = (
            self.__plot_tuple[0].plot(),
            self.__plot_tuple[1].plot(),
            self.__plot_tuple[2].plot(),
            self.__plot_tuple[3].plot(),
            self.__plot_tuple[4].plot(),
            self.__plot_tuple[5].plot(),
        )

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.__update_data_line_list)
        self.timer.start()

        self.__main_window.show()

    def __init_all_widgets(self):
        """
        This method reinitializes all widgets in the shell.

        """
        self.__load_qline()
        # self.__update_plot_widget_list()

    def __load_qline(self):
        """
        This method updates qline widtget by reading internal variable.

        """
        text = "{}:{}".format(str(self.__port_listener.get_ip()),
                            str(self.__port_listener.get_port()))

        self.__update_qline(self.__ui.ql_addr, text)

    def __init_all_connections(self):
        """
        This method initializes all connections between widget and class
            methods.

        """
        self.__ui.btn_addr.clicked.connect(self.__clicked_btn_addr)

    def __reinitialize_port_listener(self, ip, port):
        """
        This method initializes new port listener.

        """
        if self.__port_listener is not None:

            # initializes new listener object first because if it fails, old
            # one won't be touched
            try:
                new_listener = ptlr.UDPServer(ip, port)

                self.__port_listener = new_listener
                self.__plot_db.set_source_object(self.__port_listener)
                # self.__plot_db.start_processing_thread()

            except Exception as error:
                gu.log('[ERROR]: {}'.format(error.__str__()))
                self.__load_qline()

        else:
            self.__port_listener = ptlr.UDPServer(ip, port)

    def __stop_processing(self):
        """
        This method stops plot processing thread by calling
            plot_db.stop_processing method.

        """
        self.__plot_db.stop_processing()

    def __update_qline(self, qline_widget, text):
        """
        This method fills qline_widget with text.

        Keyword arguments:
        qline_widget -- < > qline widget that will be filled.
        text -- < str > text that will fill widget.

        """
        qline_widget.setText(text)

    def __update_data_line_list(self):
        """
        This method updates all graph widgets.

        """
        plot_object_list = self.__plot_db.get_plot_list()

        for index in range(self.__graph_amount):
            self.__update_data_line(
                    self.__data_list_tuple[index],
                    plot_object_list[index])

    def __update_data_line(self, data_line, plot_object, axis_range=100):
        """
        This method updates plot data line for realtime visualization.

        Keyword arguments:
        data_line -- < pyqtgraph.graphicsItems.PlotDataItem.PlotDataItem > data
            line that will be updated.
        plot_object -- < plot_db.PlotDB > plot object that will be plotted.
        ***

        """
        x = plot_object['x'][-axis_range:]
        y = plot_object['y'][-axis_range:]

        for index in range(len(x)):
            x[index] = x[index] * 1000000

        # plot_widget.setLabel('bottom', plot_widget['x_label'])
        # plot_widget.setLabel('left', plot_object['y_label'])

        data_line.setData(x, y)

    def __update_plot_widget_list(self):
        """
        This method updates all graph widgets.

        """
        plot_object_list = self.__plot_db.get_plot_list()

        for index in range(self.__graph_amount):
            self.__plot_graph(
                    self.__plot_tuple[index],
                    plot_object_list[index])

    def __plot_graph(self, plot_widget, plot_object, range=200):
        """
        This method plots the graph object on the widget.

        Keyword arguments:
        plot_widget -- < pyqtgraph.PlotWidget > plot widget that will be
            updated.

        plot_object -- < plot_db.PlotDB > plot object that will be plotted.

        """
        plot_widget.clear()

        x = plot_object['x'][-range:]
        y = plot_object['y'][-range:]

        plot_widget.setLabel('bottom', plot_object['x_label'])
        plot_widget.setLabel('left', plot_object['y_label'])

        plot_widget.plot(x, y)

    def __clicked_btn_addr(self):
        """
        This method automatically called then address button is clicked.

        """
        text = self.__ui.ql_addr.text()

        if ptlr.check_addr_correctness(text):
            self.__load_qline()
            return
        else:
            text = text.split(':')
            self.__reinitialize_port_listener(text[0], text[1])

def main():

    app = QtWidgets.QApplication(sys.argv)

    settings_dict = gu.read_json('../settings/defaults.json')

    lbe_1 = ListenerBackEnd(
                    settings_dict['ip'],
                    settings_dict['port'],
                    settings_dict['dump_save_path'])

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
