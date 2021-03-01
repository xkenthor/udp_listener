# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sources/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(824, 1003)
        MainWindow.setMinimumSize(QtCore.QSize(130, 0))
        MainWindow.setStyleSheet("\n"
"/*-----QWidget-----*/\n"
"QWidget\n"
"{\n"
"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(27, 39, 50, 255),stop:1 rgba(47, 53, 74, 255));\n"
"    color: #000000;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QLabel-----*/\n"
"QLabel\n"
"{\n"
"    background-color: transparent;\n"
"    color: #c2c7d5;\n"
"    font-size: 13px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QPushButton-----*/\n"
"QPushButton\n"
"{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.511, x2:1, y2:0.511, stop:0 rgba(0, 172, 149, 255),stop:0.995192 rgba(54, 197, 177, 255));\n"
"    color: #fff;\n"
"    font-size: 11px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"QPushButton::pressed\n"
"{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.511, x2:1, y2:0.511, stop:0 rgba(0, 207, 179, 255),stop:1 rgba(70, 255, 230, 255));\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QCheckBox-----*/\n"
"QCheckBox\n"
"{\n"
"    background-color: transparent;\n"
"    color: #fff;\n"
"    font-size: 10px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QCheckBox-----*/\n"
"QCheckBox::indicator\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid darkgray;\n"
"    width: 12px;\n"
"    height: 12px;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(\"./ressources/check.png\");\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.511, x2:1, y2:0.511, stop:0 rgba(0, 172, 149, 255),stop:0.995192 rgba(54, 197, 177, 255));;\n"
"    border: 1px solid #607cff;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:unchecked:hover\n"
"{\n"
"    border: 1px solid #08b099;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::disabled\n"
"{\n"
"    color: #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:disabled\n"
"{\n"
"    background-color: #656565;\n"
"    color: #656565;\n"
"    border: 1px solid #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QLineEdit-----*/\n"
"QLineEdit\n"
"{\n"
"    background-color: #c2c7d5;\n"
"    color: #000;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"    border-radius: 2px;\n"
"    padding: 3px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QListView-----*/\n"
"QListView\n"
"{\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(50, 61, 80, 255),stop:1 rgba(44, 49, 69, 255));\n"
"    color: #fff;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"    border: 1px solid #191919;\n"
"    show-decoration-selected: 0;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item\n"
"{\n"
"    color: #31cecb;\n"
"    background-color: #454e5e;\n"
"    border: none;\n"
"    padding: 5px;\n"
"    border-radius: 0px;\n"
"    padding-left : 10px;\n"
"    height: 42px;\n"
"\n"
"}\n"
"\n"
"QListView::item:selected\n"
"{\n"
"    color: #31cecb;\n"
"    background-color: #454e5e;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:!selected\n"
"{\n"
"    color:white;\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    padding-left : 10px;\n"
"\n"
"}\n"
"\n"
"\n"
"QListView::item:!selected:hover\n"
"{\n"
"    color: #bbbcba;\n"
"    background-color: #454e5e;\n"
"    border: none;\n"
"    padding-left : 10px;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QTreeView-----*/\n"
"QTreeView \n"
"{\n"
"    background-color: #232939;\n"
"    show-decoration-selected: 0;\n"
"    color: #c2c8d7;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::item \n"
"{\n"
"    border-top-color: transparent;\n"
"    border-bottom-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::item:hover \n"
"{\n"
"    background-color: #606060;\n"
"    color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::item:selected \n"
"{\n"
"    background-color: #0ab19a;\n"
"    color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::item:selected:active\n"
"{\n"
"    background-color: #0ab19a;\n"
"    color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings \n"
"{\n"
"    image: url(://tree-closed.png);\n"
"\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  \n"
"{\n"
"    image: url(://tree-open.png);\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QTableView & QTableWidget-----*/\n"
"QTableView\n"
"{\n"
"    background-color: #232939;\n"
"    border: 1px solid gray;\n"
"    color: #f0f0f0;\n"
"    gridline-color: #232939;\n"
"    outline : 0;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableView::disabled\n"
"{\n"
"    background-color: #242526;\n"
"    border: 1px solid #32414B;\n"
"    color: #656565;\n"
"    gridline-color: #656565;\n"
"    outline : 0;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableView::item:hover \n"
"{\n"
"    background-color: #606060;\n"
"    color: #f0f0f0;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableView::item:selected \n"
"{\n"
"    background-color: #0ab19a;\n"
"    color: #F0F0F0;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableView::item:selected:disabled\n"
"{\n"
"    background-color: #1a1b1c;\n"
"    border: 2px solid #525251;\n"
"    color: #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableCornerButton::section\n"
"{\n"
"    background-color: #343a49;\n"
"    color: #fff;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    color: #fff;\n"
"    border-top: 0px;\n"
"    border-bottom: 1px solid gray;\n"
"    border-right: 1px solid gray;\n"
"    background-color: #343a49;\n"
"    margin-top:1px;\n"
"    margin-bottom:1px;\n"
"    padding: 5px;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section:disabled\n"
"{\n"
"    background-color: #525251;\n"
"    color: #656565;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section:checked\n"
"{\n"
"    color: #fff;\n"
"    background-color: #0ab19a;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section:checked:disabled\n"
"{\n"
"    color: #656565;\n"
"    background-color: #525251;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::vertical::first,\n"
"QHeaderView::section::vertical::only-one\n"
"{\n"
"    border-top: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::vertical\n"
"{\n"
"    border-top: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::horizontal::first,\n"
"QHeaderView::section::horizontal::only-one\n"
"{\n"
"    border-left: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"QHeaderView::section::horizontal\n"
"{\n"
"    border-left: 1px solid #353635;\n"
"\n"
"}\n"
"\n"
"\n"
"/*-----QScrollBar-----*/\n"
"QScrollBar:horizontal \n"
"{\n"
"    background-color: transparent;\n"
"    height: 8px;\n"
"    margin: 0px;\n"
"    padding: 0px;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:horizontal \n"
"{\n"
"    border: none;\n"
"    min-width: 100px;\n"
"    background-color: #56576c;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:horizontal, \n"
"QScrollBar::sub-line:horizontal,\n"
"QScrollBar::add-page:horizontal, \n"
"QScrollBar::sub-page:horizontal \n"
"{\n"
"    width: 0px;\n"
"    background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar:vertical \n"
"{\n"
"    background-color: transparent;\n"
"    width: 8px;\n"
"    margin: 0;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::handle:vertical \n"
"{\n"
"    border: none;\n"
"    min-height: 100px;\n"
"    background-color: #56576c;\n"
"\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:vertical, \n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-page:vertical, \n"
"QScrollBar::sub-page:vertical \n"
"{\n"
"    height: 0px;\n"
"    background-color: transparent;\n"
"\n"
"}\n"
"")
        self.lo_mw = QtWidgets.QWidget(MainWindow)
        self.lo_mw.setObjectName("lo_mw")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.lo_mw)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lo_main = QtWidgets.QVBoxLayout()
        self.lo_main.setSpacing(6)
        self.lo_main.setObjectName("lo_main")
        self.lo_bar = QtWidgets.QHBoxLayout()
        self.lo_bar.setObjectName("lo_bar")
        self.lo_addr = QtWidgets.QVBoxLayout()
        self.lo_addr.setObjectName("lo_addr")
        self.lb_addr = QtWidgets.QLabel(self.lo_mw)
        self.lb_addr.setObjectName("lb_addr")
        self.lo_addr.addWidget(self.lb_addr)
        self.lo_1_addr = QtWidgets.QHBoxLayout()
        self.lo_1_addr.setObjectName("lo_1_addr")
        self.le_addr = QtWidgets.QLineEdit(self.lo_mw)
        self.le_addr.setMinimumSize(QtCore.QSize(155, 0))
        self.le_addr.setMaximumSize(QtCore.QSize(165, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.le_addr.setFont(font)
        self.le_addr.setObjectName("le_addr")
        self.lo_1_addr.addWidget(self.le_addr)
        self.btn_addr = QtWidgets.QPushButton(self.lo_mw)
        self.btn_addr.setMaximumSize(QtCore.QSize(130, 16777215))
        self.btn_addr.setObjectName("btn_addr")
        self.lo_1_addr.addWidget(self.btn_addr)
        self.lo_addr.addLayout(self.lo_1_addr)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lo_addr.addItem(spacerItem)
        self.lo_bar.addLayout(self.lo_addr)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lo_bar.addItem(spacerItem1)
        self.lo_oset = QtWidgets.QVBoxLayout()
        self.lo_oset.setObjectName("lo_oset")
        self.lb_buffer_size = QtWidgets.QLabel(self.lo_mw)
        self.lb_buffer_size.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lb_buffer_size.setObjectName("lb_buffer_size")
        self.lo_oset.addWidget(self.lb_buffer_size)
        self.lo_buffer_size = QtWidgets.QHBoxLayout()
        self.lo_buffer_size.setObjectName("lo_buffer_size")
        self.le_buffer_size = QtWidgets.QLineEdit(self.lo_mw)
        self.le_buffer_size.setMaximumSize(QtCore.QSize(50, 16777215))
        self.le_buffer_size.setObjectName("le_buffer_size")
        self.lo_buffer_size.addWidget(self.le_buffer_size)
        self.btn_buffer_size = QtWidgets.QPushButton(self.lo_mw)
        self.btn_buffer_size.setMaximumSize(QtCore.QSize(70, 16777215))
        self.btn_buffer_size.setObjectName("btn_buffer_size")
        self.lo_buffer_size.addWidget(self.btn_buffer_size)
        self.lo_oset.addLayout(self.lo_buffer_size)
        self.cb_history = QtWidgets.QCheckBox(self.lo_mw)
        self.cb_history.setObjectName("cb_history")
        self.lo_oset.addWidget(self.cb_history)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lo_oset.addItem(spacerItem2)
        self.lo_bar.addLayout(self.lo_oset)
        self.lo_main.addLayout(self.lo_bar)
        self.lo_pg_1 = QtWidgets.QVBoxLayout()
        self.lo_pg_1.setObjectName("lo_pg_1")
        self.lo_pt_1 = QtWidgets.QVBoxLayout()
        self.lo_pt_1.setObjectName("lo_pt_1")
        self.lb_pt_1 = QtWidgets.QLabel(self.lo_mw)
        self.lb_pt_1.setEnabled(True)
        self.lb_pt_1.setObjectName("lb_pt_1")
        self.lo_pt_1.addWidget(self.lb_pt_1)
        self.pt_1 = PlotWidget(self.lo_mw)
        self.pt_1.setMinimumSize(QtCore.QSize(0, 120))
        self.pt_1.setObjectName("pt_1")
        self.lo_pt_1.addWidget(self.pt_1)
        self.lo_pg_1.addLayout(self.lo_pt_1)
        self.lo_pt_2 = QtWidgets.QVBoxLayout()
        self.lo_pt_2.setObjectName("lo_pt_2")
        self.lb_pt_2 = QtWidgets.QLabel(self.lo_mw)
        self.lb_pt_2.setObjectName("lb_pt_2")
        self.lo_pt_2.addWidget(self.lb_pt_2)
        self.pt_2 = PlotWidget(self.lo_mw)
        self.pt_2.setMinimumSize(QtCore.QSize(0, 120))
        self.pt_2.setObjectName("pt_2")
        self.lo_pt_2.addWidget(self.pt_2)
        self.lo_pg_1.addLayout(self.lo_pt_2)
        self.lo_main.addLayout(self.lo_pg_1)
        self.lo_pg_2 = QtWidgets.QVBoxLayout()
        self.lo_pg_2.setObjectName("lo_pg_2")
        self.lo_pt_3 = QtWidgets.QVBoxLayout()
        self.lo_pt_3.setObjectName("lo_pt_3")
        self.lb_pt_3 = QtWidgets.QLabel(self.lo_mw)
        self.lb_pt_3.setObjectName("lb_pt_3")
        self.lo_pt_3.addWidget(self.lb_pt_3)
        self.pt_3 = PlotWidget(self.lo_mw)
        self.pt_3.setMinimumSize(QtCore.QSize(0, 120))
        self.pt_3.setObjectName("pt_3")
        self.lo_pt_3.addWidget(self.pt_3)
        self.lo_pg_2.addLayout(self.lo_pt_3)
        self.lo_pt_4 = QtWidgets.QVBoxLayout()
        self.lo_pt_4.setObjectName("lo_pt_4")
        self.lb_pt_4 = QtWidgets.QLabel(self.lo_mw)
        self.lb_pt_4.setObjectName("lb_pt_4")
        self.lo_pt_4.addWidget(self.lb_pt_4)
        self.pt_4 = PlotWidget(self.lo_mw)
        self.pt_4.setMinimumSize(QtCore.QSize(0, 120))
        self.pt_4.setObjectName("pt_4")
        self.lo_pt_4.addWidget(self.pt_4)
        self.lo_pg_2.addLayout(self.lo_pt_4)
        self.lo_main.addLayout(self.lo_pg_2)
        self.lo_pg_3 = QtWidgets.QVBoxLayout()
        self.lo_pg_3.setObjectName("lo_pg_3")
        self.lo_pt_5 = QtWidgets.QVBoxLayout()
        self.lo_pt_5.setObjectName("lo_pt_5")
        self.lb_pt_5 = QtWidgets.QLabel(self.lo_mw)
        self.lb_pt_5.setObjectName("lb_pt_5")
        self.lo_pt_5.addWidget(self.lb_pt_5)
        self.pt_5 = PlotWidget(self.lo_mw)
        self.pt_5.setMinimumSize(QtCore.QSize(0, 120))
        self.pt_5.setObjectName("pt_5")
        self.lo_pt_5.addWidget(self.pt_5)
        self.lo_pg_3.addLayout(self.lo_pt_5)
        self.lo_pt_6 = QtWidgets.QVBoxLayout()
        self.lo_pt_6.setObjectName("lo_pt_6")
        self.label_pt_6 = QtWidgets.QLabel(self.lo_mw)
        self.label_pt_6.setObjectName("label_pt_6")
        self.lo_pt_6.addWidget(self.label_pt_6)
        self.pt_6 = PlotWidget(self.lo_mw)
        self.pt_6.setMinimumSize(QtCore.QSize(0, 120))
        self.pt_6.setObjectName("pt_6")
        self.lo_pt_6.addWidget(self.pt_6)
        self.lo_pg_3.addLayout(self.lo_pt_6)
        self.lo_main.addLayout(self.lo_pg_3)
        self.horizontalLayout.addLayout(self.lo_main)
        MainWindow.setCentralWidget(self.lo_mw)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Plot listener"))
        self.lb_addr.setText(_translate("MainWindow", "Адрес прослушивания:"))
        self.le_addr.setText(_translate("MainWindow", "255.255.255.255:65535"))
        self.btn_addr.setText(_translate("MainWindow", "Переподключиться"))
        self.lb_buffer_size.setText(_translate("MainWindow", "Размер буферизации:"))
        self.le_buffer_size.setText(_translate("MainWindow", "99999"))
        self.btn_buffer_size.setText(_translate("MainWindow", "Изменить"))
        self.cb_history.setText(_translate("MainWindow", "Сохранять историю"))
        self.lb_pt_1.setText(_translate("MainWindow", "График №1"))
        self.lb_pt_2.setText(_translate("MainWindow", "График №2"))
        self.lb_pt_3.setText(_translate("MainWindow", "График №3"))
        self.lb_pt_4.setText(_translate("MainWindow", "График №4"))
        self.lb_pt_5.setText(_translate("MainWindow", "График №5"))
        self.label_pt_6.setText(_translate("MainWindow", "График №6"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())