from PyQt5 import QtWidgets, QtGui, QtCore
from my_tables import MyTable
from pandasmodel import PandasModel
import pandas as pd
import ccxt
import sys
import os


class DatabaseTab(QtWidgets.QWidget):
    def __init__(self, parent, zaur):
        super().__init__(parent)
        self.zaur = zaur
        self.setObjectName("Form")
        self.resize(901, 501)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 901, 486))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")


        self.tableView = MyTable(self.groupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 30, 650, 448))
        self.tableView.setObjectName("tableView")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(690, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(690, 80, 111, 31))


        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(690, 401, 200, 31))
        self.label.setFont(font)

        size = self.get_size()
        self.label.setText('Database size:')
        self.label2 = QtWidgets.QLabel(self.groupBox)
        self.label2.setGeometry(QtCore.QRect(690, 441, 200, 31))
        self.label2.setFont(font)
        self.label2.setText(f'{size} MB')


        self.current_exchange = None

        try:
            self.update_tables()
        except:
            pass

        self.retranslateUi()

        self.pushButton.clicked.connect(self.update_tables)
        self.pushButton_2.clicked.connect(self.drop_table)
        QtCore.QMetaObject.connectSlotsByName(self)


    def get_size(self):
        return (os.stat(self.zaur.db.database).st_size / 1000000).__round__(3)

    def update_tables(self):
        tables = self.zaur.db.table_list()
        t = []

        for table in tables:
            if '_' in table[0]:
                t.append(table[0])

        self.tables = pd.DataFrame(index=t, columns=['start date', 'end date'])

        for table in t:
            start = self.zaur.db.execute_read_query(f"""SELECT MIN("Date") FROM '{table}';""")[0][0]
            end = self.zaur.db.execute_read_query(f"""SELECT MAX("Date") FROM '{table}';""")[0][0]
            self.tables.loc[table, 'start date'] = ccxt.Exchange.iso8601(start)[:16].replace('T', ' ')
            self.tables.loc[table, 'end date'] = ccxt.Exchange.iso8601(end)[:16].replace('T', ' ')

        self.model = PandasModel(self.tables)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 175)
        self.tableView.setColumnWidth(1, 175)
        size = self.get_size()
        self.label2.setText(f'{size} MB')


    def drop_table(self):
        current_index = self.tableView.currentIndex().row()
        table_name = self.tables.index[current_index]
        self.zaur.db.drop_table(table_name)
        self.tables.drop(table_name, inplace=True)
        self.model = PandasModel(self.tables)
        self.tableView.setModel(self.model)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "  database"))
        self.pushButton.setText(_translate("Form", "update"))
        self.pushButton_2.setText(_translate("Form", "delete"))

