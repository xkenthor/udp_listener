"""
This module implements backend logic for graphical shell and connects it with
    core modules.

"""
import threading
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

    def __init__(self, settings_path):
        """
        This method implements backend logic for graphical shell.

        """
        # GIGACRUTCH
        self.__counter_list = [0,0,0,0,0,0]

        settings_dict = gu.read_json(settings_path)
        self.__th_lock_settings_file = threading.Lock()

        self.__settings_path = settings_path
        self.__settings_dict = settings_dict
        self.__graph_amount = 6

        self.__port_listener = ptlr.UDPServer(
                                self.__settings_dict['ip'],
                                self.__settings_dict['port'])

        self.__plot_db = ptdb.PlotDB(
                                self.__port_listener,
                                self.__graph_amount,
                                self.__settings_dict['dump_save_dir'],
                                self.__settings_dict['dumping_enabled'],
                                self.__settings_dict['default_plot_backup'],
                                self.__settings_dict['default_plot_thresh'])

        self.__set_buffer_size(self.__settings_dict['buffer_size'])

        self.__plot_db.start_processing_thread()

        self.__main_window = QtWidgets.QMainWindow()
        self.__main_window.resize(824, 1005)
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

    def __del__(self):# exit__(self, exc_type, exc_value, traceback):
        """
        This method stops processing port and plot_db.

        """
        self.__plot_db.stop_processing()
        self.__port_listener.stop_service()

    def __init_all_connections(self):
        """
        This method initializes all connections between widget and class
            methods.

        """
        self.__ui.btn_addr.clicked.connect(self.__clicked_btn_addr)
        self.__ui.btn_buffer_size.clicked.connect(
                                                self.__clicked_btn_buffer_size)
        self.__ui.cb_history.clicked.connect(self.__clicked_cb_history)

    def __init_all_widgets(self):
        """
        This method reinitializes all widgets in the shell.

        """
        # self.__update_plot_widget_list()
        self.__load_le_addr()
        self.__load_le_buffer_size()
        self.__load_cb_history()

    def __load_le_addr(self):
        """
        This method updates le_addr widget by reading internal variable.

        """
        text = "{}:{}".format(str(self.__port_listener.get_ip()),
                            str(self.__port_listener.get_port()))

        self.__update_line_edit(self.__ui.le_addr, text)

    def __load_le_buffer_size(self):
        """
        This method updates le_buffer_size widget by reading internal variable.

        """
        self.__update_line_edit(self.__ui.le_buffer_size,
                                    str(self.__settings_dict['buffer_size']))

    def __load_cb_history(self):
        """
        This method updates cb_history widget by reading internal variable.

        """
        if self.__settings_dict['dumping_enabled']:
            self.__ui.cb_history.setChecked(True)
        else:
            self.__ui.cb_history.setChecked(False)

    def __set_buffer_size(self, buffer_size):
        """
        This method changes buffer_size, checks its range and saves it to
            settings_dict.

        buffer_size -- < int > new buffer_size.0

        """
        lower_limit = 3
        upper_limit = 10000

        try:
            buffer_size = int(buffer_size)

            if buffer_size < lower_limit or buffer_size > upper_limit:
                raise ValueError(
                    'Buffer size is out of [{}, {}] limit.'.format(
                                                    lower_limit, upper_limit))

            self.__buffer_size = buffer_size
            self.__settings_dict['buffer_size'] = buffer_size

            self.__dump_settings()

        except Exception as error:
            gu.log(error.__str__(), 1)

            self.__load_le_buffer_size()

    def __dump_settings(self):
        """
        This method simply saves current settings_dict to settings file.

        """
        self.__th_lock_settings_file.acquire()
        gu.write_json(self.__settings_path, self.__settings_dict)
        self.__th_lock_settings_file.release()

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

                self.__settings_dict['ip'] = ip
                self.__settings_dict['port'] = port


            except Exception as error:
                gu.log('[ERROR]: {}'.format(error.__str__()))
                self.__load_le_addr()

        else:
            self.__port_listener = ptlr.UDPServer(ip, port)

    def __stop_processing(self):
        """
        This method stops plot processing thread by calling
            plot_db.stop_processing method.

        """
        self.__plot_db.stop_processing()

    def __update_line_edit(self, line_edit_widget, text):
        """
        This method fills line_edit_widget with text.

        Keyword arguments:
        line_edit_widget -- < > line_edit widget that will be filled.
        text -- < str > text that will fill widget.

        """
        line_edit_widget.setText(text)

    def __update_data_line_list(self):
        """
        This method updates all graph widgets.

        """
        plot_object_list = self.__plot_db.get_plot_list()

        for index in range(self.__graph_amount):
            self.__update_data_line(
                    self.__data_list_tuple[index],
                    plot_object_list[index],
                    index)

    def __update_data_line(self, data_line, plot_object, plot_index):
        """
        This method updates plot data line for realtime visualization.

        Keyword arguments:
        data_line -- < pyqtgraph.graphicsItems.PlotDataItem.PlotDataItem > data
            line that will be updated.
        plot_object -- < plot_db.PlotDB > plot object that will be plotted.

        """
        # x = plot_object['x'][-self.__buffer_size:]
        y = plot_object['y'][-self.__buffer_size:]

        modifier = 0.00001
        x = list(range(len(y)))
        for index in x:
            x[index] = x[index]*modifier + self.__counter_list[plot_index]

        self.__counter_list[plot_index] += modifier*len(y)

        # for index in range(len(x)):
        #     x[index] = x[index] * 1000000

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

    def __plot_graph(self, plot_widget, plot_object):
        """
        This method plots the graph object on the widget.

        Keyword arguments:
        plot_widget -- < pyqtgraph.PlotWidget > plot widget that will be
            updated.
        plot_object -- < plot_db.PlotDB > plot object that will be plotted.

        """
        plot_widget.clear()

        x = plot_object['x'][-self.__buffer_size:]
        y = plot_object['y'][-self.__buffer_size:]

        plot_widget.setLabel('bottom', plot_object['x_label'])
        plot_widget.setLabel('left', plot_object['y_label'])

        plot_widget.plot(x, y)

    def __clicked_btn_addr(self):
        """
        This method automatically called then address button is clicked.

        """
        text = self.__ui.le_addr.text()

        if ptlr.check_addr_correctness(text):
            self.__load_le_addr()
            return
        else:
            text = text.split(':')
            self.__reinitialize_port_listener(text[0], text[1])

    def __clicked_cb_history(self):
        """
        This method automatically called then history checkbox is clicked.

        """
        flag = self.__ui.cb_history.isChecked()

        if flag != self.__settings_dict['dumping_enabled']:
            self.__plot_db.set_dumping_enable_flag(flag)
            self.__settings_dict['dumping_enabled'] = flag
            self.__dump_settings()

    def __clicked_btn_buffer_size(self):
        """
        This method automatically called then buffer button is clicked.

        """
        text = self.__ui.le_buffer_size.text()
        self.__set_buffer_size(text)

def main():

    app = QtWidgets.QApplication(sys.argv)

    lbe_1 = ListenerBackEnd('../settings/defaults.json')

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
