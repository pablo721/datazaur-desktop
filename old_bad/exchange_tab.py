
from my_tables import DataTable, MyTable
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import ccxt
import numpy as np
from pandasmodel import PandasModel
from database import Database

# a tab containing 1 exchange
class ExchangeTab(QtWidgets.QWidget):
    def __init__(self, parent, exchange, zaur):
        super().__init__(parent)
        self.zaur = zaur
        self.exchange = exchange
        self.tickers = exchange.symbols
        self.df = pd.DataFrame(index=self.tickers, columns=['price', '24h Δ', 'vol'])
        self.filter = False
        self.setGeometry(QtCore.QRect(0, 0, 401, 451))
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 401, 451))

        self.tabs = QtWidgets.QTabWidget(self.frame)
        self.tabs.setGeometry(QtCore.QRect(0, 50, 401, 451))

        self.markets_tab = MyTab(self.tabs)
        self.markets_table = DataTable(self.markets_tab, self.df)


        self.info_tab = MyTab(self.tabs)
        self.info_table = MyTable(self.info_tab)
        self.info_table.setGeometry(QtCore.QRect(0, 0, 396, 392))
        model = PandasModel(pd.DataFrame(data={'info': self.exchange.has.values()}, index=self.exchange.has.keys()))
        self.info_table.setModel(model)
        self.info_table.setSortingEnabled(False)
        self.info_table.setColumnWidth(0, 140)

        self.account_tab = AccountTab(self, self.zaur)
        self.wallet_tab = MyTab(self.tabs)
        self.wallet_table = MyTable(self.wallet_tab)
        self.wallet_table.setGeometry(QtCore.QRect(0, 0, 396, 392))


        self.tabs.addTab(self.markets_tab, 'markets')
        self.tabs.addTab(self.account_tab, 'keys')
        self.tabs.addTab(self.wallet_tab, 'wallet')
        self.tabs.addTab(self.info_tab, 'info')

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 10, 150, 31))
        self.label.setText(f'total tickers: {len(self.tickers)}')
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(150, 10, 80, 31))
        self.pushButton.setText('fetch all')
        self.linijka = QtWidgets.QLineEdit(self.frame)
        self.linijka.setGeometry(QtCore.QRect(300, 10, 90, 31))
        self.linijka.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                           "alternate-background-color: rgb(9, 21, 32); \n"
                           "color: rgb(255, 255, 255); \n"
                           "font: 50  10pt \"FreeMono Bold\";")

        try:
            self.fetch_balance()
        except:
            pass

        #self.markets_table.clicked.connect(self.select_ticker)
        self.markets_table.pressed.connect(self.select_ticker)
        self.linijka.textChanged.connect(self.filter_tickers)
        self.pushButton.clicked.connect(self.fetch_all)

    # gets account balance
    def fetch_balance(self):
        df = self.zaur.fetch_balance(self.exchange.id)
        model = PandasModel(df)
        self.wallet_table.setModel(model)

    # method for ticker selection
    def select_ticker(self):
        current_index = self.markets_table.currentIndex().row()
        if self.filter:
            current_ticker = self.df2.index[current_index]
        else:
            current_ticker = self.df.index[current_index]

        self.zaur.front.select_ticker(current_ticker)

    # gets prices for all tickers on current exchange (not all exchages allow this)
    def fetch_all(self):
        try:
            data = pd.DataFrame(self.exchange.fetchTickers()).transpose()
            d2 = data.loc[:, ['last', 'percentage', 'baseVolume']]
            d2.columns = ['price', '24h Δ', 'vol']
            self.df.update(d2)
            self.markets_table.update_data(self.df)
            self.zaur.market_data[self.exchange.id] = data
            data.to_csv('data1566.csv')
        except Exception as e:
            print(f'error {e}')



    # rounds data
    def round_data(self):
        self.df.loc[:, ['24h Δ', 'vol']] = self.df.loc[:, ['24h Δ', 'vol']].round(2)
        self.df['price'] = self.df['price'].round(4)

    # filter tickers
    def filter_tickers(self):
        text = self.linijka.text()
        self.df2 = self.df.loc[filter(lambda x: text.replace('/', '').upper() in x.replace('/', '').upper(), self.df.index)]
        model = PandasModel(self.df2)
        self.markets_table.setModel(model)

        if len(text) > 0:
            self.filter = True
            self.label.setText(f'search: {text}: {len(self.df2)}')
        else:
            self.filter = False
            self.label.setText(f'total tickers: {len(self.tickers)}')



class MyTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 30, 393, 415))
        self.setStyleSheet("background-color: rgb(0, 18, 36); \n"
                           "alternate-background-color: rgb(9, 21, 32); \n"
                           "color: rgb(255, 255, 255); \n"
                           "font: 50  10pt \"FreeMono Bold\";")


# tab where you save your keys
class AccountTab(QtWidgets.QWidget):
    def __init__(self, parent, zaur):

        super().__init__(parent)
        self.zaur = zaur
        self.parent = parent
        self.setGeometry(QtCore.QRect(0, 0, 401, 415))
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 401, 415))
        self.frame.setStyleSheet("background-color: rgb(0, 18, 36); \n"
                               "alternate-background-color: rgb(9, 21, 32); \n"
                               "color: rgb(255, 255, 255); \n"
                               "font: 50  10pt \"FreeMono Bold\";")





        self.pubkey_label = QtWidgets.QLabel(self.frame)
        self.pubkey_label.setGeometry(QtCore.QRect(5, 20, 300, 31))
        self.pubkey_label.setText('public API key')
        self.pubkey_line = QtWidgets.QLineEdit(self.frame)
        self.pubkey_line.setGeometry(QtCore.QRect(5, 55, 300, 31))
        #self.pubkey_line.setInputMask(QtGui.QInpu)


        self.privkey_label = QtWidgets.QLabel(self.frame)
        self.privkey_label.setGeometry(QtCore.QRect(5, 100, 300, 31))
        self.privkey_label.setText('private API key')
        self.privkey_line = QtWidgets.QLineEdit(self.frame)
        self.privkey_line.setGeometry(QtCore.QRect(5, 136, 300, 31))
        #self.privkey_line.setInputMask(QtGui.QInpu)

        self.password_label = QtWidgets.QLabel(self.frame)
        self.password_label.setGeometry(QtCore.QRect(5, 181, 300, 31))
        self.password_label.setText('password')
        self.password_line = QtWidgets.QLineEdit(self.frame)
        self.password_line.setGeometry(QtCore.QRect(5, 216, 300, 31))
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)

        self.save_button = QtWidgets.QPushButton(self.frame)
        self.save_button.setGeometry(QtCore.QRect(220, 270, 80, 31))
        self.save_button.setText('save keys')

        #self.show_button = QtWidgets.QPushButton(self.frame)
        #self.show_button.setGeometry(QtCore.QRect(5, 250, 80, 31))
        #self.show_button.setText('show keys')


        self.logout_button = QtWidgets.QPushButton(self.frame)
        self.logout_button.setGeometry(QtCore.QRect(250, 400, 80, 31))
        self.logout_button.setText('logout')


        self.save_button.clicked.connect(self.save_keys)
        #self.show_button.clicked.connect(self.show_keys)
        self.logout_button.clicked.connect(self.logout)

        for line in [self.pubkey_line, self.privkey_line, self.password_line]:
            line.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                           "alternate-background-color: rgb(9, 21, 32); \n"
                           "color: rgb(255, 255, 255); \n"
                           "font: 50  10pt \"FreeMono Bold\";")


    def logout(self):
        pass


    def show_keys(self):
        pass

    # saves API keys
    def save_keys(self):
        pubkey = self.pubkey_line.text()
        privkey = self.privkey_line.text()
        password = self.password_line.text()

        if self.zaur.check_hash(self.zaur.front.user, password):

            query = f"SELECT user FROM keys WHERE exchange='{self.zaur.current_exchange.id}' AND user='{self.zaur.user}'"
            keycheck = self.zaur.db.execute_read_query(query)

            print(keycheck)

            if keycheck:
                dialog = QtWidgets.QMessageBox()
                dialog.setText('Keys are already saved for this exchange.')
                dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 75 11pt \"FreeMono Bold\";")
                dialog.exec_()
                return

            else:

                self.zaur.add_keys(pubkey, privkey, password)
                dialog = QtWidgets.QMessageBox()
                dialog.setText('Keys saved.')
                dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 75 11pt \"FreeMono Bold\";")
                dialog.exec_()
                self.parent.fetch_balance()

        else:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Wrong password.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            return






























































