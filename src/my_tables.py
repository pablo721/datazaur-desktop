

from PyQt5 import QtWidgets, QtCore
from pandasmodel import PandasModel
import pandas as pd


class MyTable(QtWidgets.QTableView):
    def __init__(self, parent):
        super().__init__(parent)

        self.setGeometry(QtCore.QRect(0, 0, 891, 451))
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Ubuntu Condensed\";")

    @staticmethod
    def round_data(df, columns, decimals):
        for col in columns:
            df.loc[:, col] = df.loc[:, col].round(decimals)
        return df

    def add_data(self, df):
        model = PandasModel(df)
        self.setModel(model)



class QuoteTable(QtWidgets.QTableView):
    def __init__(self, parent):
        super().__init__(parent)

        self.setSortingEnabled(False)
        self.quote = None
        self.df = pd.DataFrame(data=None, columns=['price', '24h Δ', '24h high', '24h low', 'vol'], index = [0])
        self.setGeometry(QtCore.QRect(-12, 21, 399, 60))
        model = PandasModel(self.df)
        self.setModel(model)

        self.resize_columns()

    def set_quote(self, data):
        self.df.iloc[0] = data
        model = PandasModel(self.df)
        self.setModel(model)

    def resize_columns(self):
        self.setColumnWidth(0, 90)
        self.setColumnWidth(1, 40)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 80)
        self.setColumnWidth(4, 80)





class DataTable(QtWidgets.QTableView):
    def __init__(self, parent, df):
        super().__init__(parent)

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")

        self.df = df.copy()
        self.df2 = df.copy()
        self.df.columns = ['price', '24h Δ', 'vol']
        self.df.index = self.df.index.map(lambda x: x[:10])
        self.sortByColumn(3, QtCore.Qt.DescendingOrder)


        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self.setGeometry(QtCore.QRect(0, 0, 396, 392))
        self.round_data()
        #self.df['24h Δ'] = self.df['24h Δ'].apply(lambda x: f'{x}%')

        model = PandasModel(self.df)
        self.setModel(model)
        self.resize_columns()


    def resize_columns(self):
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)




    def update_data(self, df):
        self.df.update(df)
        self.round_data()
        m3 = PandasModel(self.df)
        self.setModel(m3)


    def round_data(self):
        self.df[['24h Δ', 'vol']] = self.df[['24h Δ', 'vol']].astype('float64').round(2)
        self.df[['price']] = self.df[['price']].astype('float64').round(4)


