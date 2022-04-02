import finplot as fplt
import yfinance
from PyQt5 import QtCore, QtWidgets
import sys
import pandas as pd
import ta
from ccxt import Exchange
import numpy as np
import time
import requests
from io import StringIO

# chart displaying widget
class ChartWidget(QtWidgets.QWidget):
    def __init__(self, parent, zaur):
        super().__init__(parent)
        self.zaur = zaur
        self.axes = dict()
        self.setGeometry(QtCore.QRect(0, 0, 901, 461))
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 901, 461))

        self.frame.setStyleSheet("alternate-background-color: rgb(8, 24, 22);\n"
                                   "background-color: rgb(10, 20, 40);\n"
                                "color: rgb(255, 255, 255);\n"
                                "font: 75 11pt \"Freemono Bold\";")
        self._timeframe='1M'
        self._interval='1h'

        self.current_tab = None

        self.tabs = QtWidgets.QTabWidget(self.frame)
        self.tabs.setGeometry(QtCore.QRect(0, 0, 901, 461))
        self.tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabs.setMovable(True)



    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, i):
        self._interval = i

    @property
    def timeframe(self):
        return self.timeframe

    @timeframe.setter
    def timeframe(self, t):
        self._timeframe = t


    def ohlc_chart(self, df):
        tab = OHLCChart(df, self)
        self.tabs.addTab(tab, df.name)
        self.tabs.setCurrentIndex(-1)


    def prepare_df_line(self, df):
        df2 = df.copy()
        df2.columns = ['Date', df.name]
        return df2


    def create_line_chart(self, df):
        df2 = self.prepare_df_log(df)
        self.lineChart = LineChart(df2)
        self.tabs.addTab(self.lineChart, df.name)

        #self.lineChart.add_line(self.log_df)


    def new_line(self, df):
        df2 = self.prepare_df_log(df)
        self.lineChart.add_line(df2)




# chart with multiple lines
class MultiLineChart(QtWidgets.QWidget):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 10, 831, 481))

        self.lines = dict()
        self.df = df

        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.resize(765, 545)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.graph)
        self.set_colors()

        self.ax = fplt.create_plot(init_zoom_periods=100, maximize=True, rows=1)

        #fplt.plot(self.df, ax=self.ax)

        self.ax.getAxis('right').show()
        self.ax.getAxis('left').hide()

        self.ax.showGrid(x=True, y=True, alpha=0.3)
        self.hover_label = fplt.add_legend('', ax=self.ax)
        self.layout.addWidget(self.ax.vb.win)
        self.graph.axs = [self.ax]

        fplt.side_margin = 0
        fplt.y_label_width = 60

        fplt.set_time_inspector(self.update_legend, ax=self.ax, when='hover')




        for col in self.df.columns:
            fplt.plot(self.df[col], ax=self.ax)

        self.graph.axs = [self.ax]
        self.layout.addWidget(self.ax.vb.win, 0, 0, 3, 2)
        fplt.show(qt_exec=False)


    # adds new line to chart
    def add_line(self, df):
        df.set_index('Date', inplace=True)
        self.df[df.name] = df[df.name]
        fplt.plot(df[df.name], ax=self.ax)
        fplt.show(qt_exec=False)

    # sets colors
    def set_colors(self):
        self.setStyleSheet("background-color: rgb(5, 16, 36);\n"
                                 "color: rgb(255, 255, 255);\n"
                                "border-color: rgb(0, 0, 0);\n"
                                 "")
        fplt.background = '#000e19'
        fplt.foreground = '#EFFBF8'
        fplt.cross_hair_color = '#EFFBF8'

    # updates legend
    def update_legend(self, x, y):
        row = self.df.loc[x/1000000]
        col0 = self.df.columns[0]
        col1 = self.df.columns[1]
        col2 = self.df.columns[2]

        fmt1 = '<span style="color:#%s">%%s</span>' % '0052ff'
        fmt2 = '<span style="color:#%s">%%.2f</span>' % '0052ff'
        fmt3 = '<span style="color:#%s">%%s</span>' % 'c48800'
        fmt4 = '<span style="color:#%s">%%.2f</span>' % 'c48800'
        fmt5 = '<span style="color:#%s">%%s</span>' % '00c425'
        fmt6 = '<span style="color:#%s">%%.2f</span>' % '00c425'

        text = '%s: %s %s: %s %s: %s' % (fmt1, fmt2, fmt3, fmt4, fmt5, fmt6)

        self.hover_label.setText(text % (col0, row[col0].__round__(2), col1, row[col1].__round__(2), col2, row[col2].__round__(2)))

        legend = f"{col0}: {row[col0].__round__(2)}    {col1}: {row[col1].round(2)}"

        #self.hover_label.setText(legend)



# single line chart
class LineChart(QtWidgets.QWidget):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 10, 835, 481))

        self.lines = dict()
        self.df = df


        #self.df.set_index('Date', inplace=True)

        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.resize(765, 545)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.graph)
        self.set_colors()

        self.ax = fplt.create_plot(init_zoom_periods=100, maximize=True, rows=1)
        #fplt.plot(self.df, ax=self.ax)

        self.ax.getAxis('right').show()
        self.ax.getAxis('left').hide()

        self.ax.showGrid(x=True, y=True, alpha=0.3)
        self.hover_label = fplt.add_legend('', ax=self.ax)
        self.layout.addWidget(self.ax.vb.win)
        self.graph.axs = [self.ax]

        fplt.side_margin = 0
        fplt.y_label_width = 0

        fplt.set_time_inspector(self.update_legend, ax=self.ax, when='hover')



        fplt.plot(self.df, ax=self.ax)

        self.graph.axs = [self.ax]
        self.layout.addWidget(self.ax.vb.win, 0, 0, 3, 2)
        fplt.show(qt_exec=False)

    # sets colors
    def set_colors(self):
        self.setStyleSheet("background-color: rgb(5, 16, 36);\n"
                                  "color: rgb(255, 255, 255);\n"
                                  "border-color: rgb(0, 0, 0);\n")

        fplt.draw_line_color = '#ffffff'
        fplt.background = '#000e19'
        fplt.foreground = '#EFFBF8'
        fplt.cross_hair_color = '#EFFBF8'
        fplt.candle_bear_color = '#bd0000'
        fplt.candle_bull_body_color = '#000f14'
        fplt.candle_bear_body_color = '#ffffff'

    # updates legend
    def update_legend(self, x, y):
        row = self.df.loc[x/1000000]
        self.hover_label.setText(f'{self.df.name}: {row[self.df.columns[0]].__round__(3)}')



# OHLC chart
class OHLCChart(QtWidgets.QWidget):
    def __init__(self, df, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, 903, 460))
        self.df = df.copy()
        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.resize(903, 460)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.graph)
        self.setStyleSheet("background-color: rgb(5, 16, 36);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "border-color: rgb(0, 0, 0);\n")

        self.set_colors()
        self.ax = fplt.create_plot(init_zoom_periods=100, maximize=True, rows=1)
        fplt.candlestick_ochl(self.df['Open Close High Low'.split()], ax=self.ax)
        self.axo = self.ax.overlay()
        fplt.volume_ocv(self.df['Open Close Volume'.split()], ax=self.axo)
        self.ax.getAxis('right').show()
        self.ax.getAxis('left').hide()

        self.ax.showGrid(x=True, y=True, alpha=0.4)

        self.hover_label = fplt.add_legend('', ax=self.ax)
        self.layout.addWidget(self.ax.vb.win)
        self.graph.axs = [self.ax]
        fplt.side_margin = 0
        fplt.y_label_width = 100

        self.layout.addWidget(self.ax.vb.win, 0, 0, 3, 2)

        fplt.set_time_inspector(self.update_legend, ax=self.ax, when='hover')
        fplt.add_crosshair_info(self.update_crosshair_info, ax=self.ax)
        fplt.show(qt_exec=False)

    # updates legend
    def update_legend(self, x, y):
        row = self.df.loc[x/1000000]
        fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open < row.Close).all() else 'a00')
        text = 'O %s H %s L %s C %s Vol %s' % (fmt, fmt, fmt, fmt, fmt)
        self.hover_label.setText(text % (row.Open, row.High, row.Low, row.Close, row.Volume))

    # updates crosshair info
    def update_crosshair_info(self, x, y, xtext, ytext):
        ytext = '%s (Close%+.2f)' % (ytext, (y - self.df.iloc[x].Close))
        return xtext, ytext

    def add_ma(self):
        pass

    # add technical indicator
    def add_indicator(self):
        indicator = self.combo.currentText()
        ax2 = fplt.create_plot(init_zoom_periods=10, maximize=False)
        self.graf.axs.append(ax2)
        
        if indicator == 'MACD':
            macd = self.df.Close.ewm(span=12).mean() - self.df.Close.ewm(span=26).mean()
            signal = macd.ewm(span=9).mean()
            self.df['macd_diff'] = macd - signal
            fplt.volume_ocv(self.df[['Date', 'Open', 'Close', 'macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)
            fplt.plot(macd, ax=ax2, legend='MACD')
            fplt.plot(signal, ax=ax2, legend='Signal')
            

        elif indicator == 'RSI':
            rsi = ta.momentum.rsi(self.df['Close'], fillna=True)
            fplt.plot(rsi, ax=ax2, legend='RSI')

    # sets colors
    def set_colors(self):
        fplt.background = '#000e19'
        fplt.foreground = '#EFFBF8'
        fplt.cross_hair_color = '#EFFBF8'
        fplt.candle_bear_color = '#bd0000'
        fplt.candle_bull_body_color = '#000f14'
        fplt.candle_bear_body_color = '#ffffff'




# OHLC chart in a new window
class ChartWindow(QtWidgets.QWidget):
    def __init__(self, df):
        super().__init__()
        self.setGeometry(QtCore.QRect(0, 0, 903, 460))
        self.df = df.copy()
        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.resize(903, 460)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.graph)
        self.setStyleSheet("background-color: rgb(5, 16, 36);\n"
                           "color: rgb(255, 255, 255);\n"
                           "border-color: rgb(0, 0, 0);\n")

        self.set_colors()
        self.ax = fplt.create_plot(init_zoom_periods=100, maximize=True, rows=1)
        fplt.candlestick_ochl(self.df['Open Close High Low'.split()], ax=self.ax)
        self.axo = self.ax.overlay()
        fplt.volume_ocv(self.df['Open Close Volume'.split()], ax=self.axo)
        self.ax.getAxis('right').show()
        self.ax.getAxis('left').hide()

        self.ax.showGrid(x=True, y=True, alpha=0.4)

        self.hover_label = fplt.add_legend('', ax=self.ax)
        self.layout.addWidget(self.ax.vb.win)
        self.graph.axs = [self.ax]
        fplt.side_margin = 0
        fplt.y_label_width = 100

        self.layout.addWidget(self.ax.vb.win, 0, 0, 3, 2)

        fplt.set_time_inspector(self.update_legend, ax=self.ax, when='hover')
        fplt.add_crosshair_info(self.update_crosshair_info, ax=self.ax)
        fplt.show(qt_exec=False)

    # updates legend
    def update_legend(self, x, y):
        row = self.df.loc[x / 1000000]
        fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open < row.Close).all() else 'a00')
        text = 'O %s H %s L %s C %s Vol %s' % (fmt, fmt, fmt, fmt, fmt)
        self.hover_label.setText(text % (row.Open, row.High, row.Low, row.Close, row.Volume))

    # updates crosshard info
    def update_crosshair_info(self, x, y, xtext, ytext):
        ytext = '%s (Close%+.2f)' % (ytext, (y - self.df.iloc[x].Close))
        return xtext, ytext

    def add_ma(self):
        pass

    # adds technical indicator
    def add_indicator(self):
        indicator = self.combo.currentText()
        ax2 = fplt.create_plot(init_zoom_periods=10, maximize=False)
        self.graf.axs.append(ax2)

        if indicator == 'MACD':
            macd = self.df.Close.ewm(span=12).mean() - self.df.Close.ewm(span=26).mean()
            signal = macd.ewm(span=9).mean()
            self.df['macd_diff'] = macd - signal
            fplt.volume_ocv(self.df[['Date', 'Open', 'Close', 'macd_diff']], ax=ax2,
                            colorfunc=fplt.strength_colorfilter)
            fplt.plot(macd, ax=ax2, legend='MACD')
            fplt.plot(signal, ax=ax2, legend='Signal')


        elif indicator == 'RSI':
            rsi = ta.momentum.rsi(self.df['Close'], fillna=True)
            fplt.plot(rsi, ax=ax2, legend='RSI')

    #sets colors
    def set_colors(self):
        fplt.background = '#000e19'
        fplt.foreground = '#EFFBF8'
        fplt.cross_hair_color = '#EFFBF8'
        fplt.candle_bear_color = '#bd0000'
        fplt.candle_bull_body_color = '#000f14'
        fplt.candle_bear_body_color = '#ffffff'







