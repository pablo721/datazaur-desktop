
import pandas as pd
import numpy as np
from pandasmodel import PandasModel
from PyQt5 import QtWidgets, QtCore, QtGui
from my_charts import LineChart, MultiLineChart
from my_tables import MyTable
from statarb_algo import StatArbAlgorithm
import os

# Tabwidget with Engle-Granger test results
class EGTabs(QtWidgets.QTabWidget):
    def __init__(self, parent, tests, summary, df, resid, corr_matrix):
        super().__init__(parent)

        self.parenttabs = parent
        self.setGeometry(QtCore.QRect(0, 10, 901, 500))
        self.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Ubuntu Condensed\";")
        df.name = 'line chart'
        resid_df = pd.DataFrame(resid)
        resid_df.name = 'OLS residuals'
        z_score = pd.DataFrame((resid - np.mean(resid)) / np.std(resid))
        z_score.name = 'z_score'


        self.lines_chart = MultiLineChart(self, df)
        self.z_score_chart = LineChart(self, z_score)
        self.ols_resid = LineChart(self, resid_df)

        self.stats_tab = QtWidgets.QWidget(self)
        self.stats_tab.setGeometry(QtCore.QRect(0, 0, 901, 470))

        ols_results = summary.tables[0].as_html()
        ols_df = pd.read_html(ols_results, index_col=0)[0]
        coef_results = summary.tables[1].as_html()
        coef_df = pd.read_html(coef_results, header=0, index_col=0)[0]

        ols_table = MyTable(self.stats_tab)
        ols_table.setSortingEnabled(False)
        ols_table.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Ubuntu Condensed\";")
        ols_table.setGeometry(QtCore.QRect(0, 0, 458, 273))
        ols_table.setModel(PandasModel(ols_df))
        ols_table.horizontalHeader().hide()

        coef_table = MyTable(self.stats_tab)
        coef_table.setSortingEnabled(False)
        coef_table.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Ubuntu Condensed\";")
        coef_table.setGeometry(QtCore.QRect(0, 275, 692, 161))
        coef_table.setModel(PandasModel(coef_df))

        test_table = MyTable(self.stats_tab)
        test_table.setSortingEnabled(False)
        test_table.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Ubuntu Condensed\";")
        test_table.setGeometry(QtCore.QRect(485, 0, 240, 90))
        model = PandasModel(pd.DataFrame(tests))
        test_table.setModel(model)

        corr_table = MyTable(self.stats_tab)
        corr_table.setSortingEnabled(False)
        corr_table.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Ubuntu Condensed\";")
        self.corr_matrix = corr_matrix.copy()
        self.corr_matrix.index.name = 'corr matrix'
        corr_table.setGeometry(QtCore.QRect(485, 110, 80+120*len(self.corr_matrix), 30+30*len(self.corr_matrix)))
        model = PandasModel(self.corr_matrix)
        corr_table.setModel(model)

        self.pushButton_40 = QtWidgets.QPushButton(self)
        self.pushButton_40.setGeometry(QtCore.QRect(810, 0, 71, 31))
        self.pushButton_40.setObjectName("pushButton_40")
        self.pushButton_40.setText("close")

        #self.button2 = QtWidgets.QPushButton(self.stats_tab)
        #self.button2.setGeometry(QtCore.QRect(10, 410, 80, 60))
        #self.button2.setText("save result")

        self.addTab(self.stats_tab, "EG-test")
        self.addTab(self.lines_chart, "lines chart")
        self.addTab(self.ols_resid, "ols residuals (spread)")
        self.addTab(self.z_score_chart, "z-score")

        #self.button2.clicked.connect(self.save_results)
        self.pushButton_40.clicked.connect(self.close_analysis)


    # closes tab
    def close_analysis(self):
        self.parenttabs.removeTab(self.parenttabs.currentIndex())

    # saves result to file
    def save_results(self):
        try:
            results = pd.read_csv('EG_tests.csv', index=True)
            results.iloc[len(results)] = self.results
            results.to_csv('EG_tests.csv')

        except FileNotFoundError:
            results = pd.DataFrame(columns=[self.results.index.values])
            results.iloc[0] = self.results
            results.to_csv('EG_tests.csv')




# Tabwidget with backtest logs and result
class BacktestTabs(QtWidgets.QTabWidget):
    def __init__(self, parent, df, results, z_score):
        super().__init__(parent)

        self.parenttabs = parent
        self.setGeometry(QtCore.QRect(0, 10, 901, 500))
        self.setStyleSheet("font: 75 11pt \"FreeMono Bold\";\n"
                            "background-color: rgb(20, 20, 40);\n"
                            "color: rgb(255, 255, 255);")

        self.logs_tab = QtWidgets.QWidget(self)
        self.logs_tab.setGeometry(QtCore.QRect(0, 0, 901, 470))
        self.logs_table = MyTable(self.logs_tab)
        self.logs_table.setGeometry(QtCore.QRect(0, 0, 893, 414))
        self.logs_table.setSortingEnabled(False)
        self.logs_table.setModel(PandasModel(df))
        self.logs_table.setColumnWidth(0, 160)

        self.results_tab = QtWidgets.QWidget(self)
        self.results_tab.setGeometry(QtCore.QRect(0, 0, 901, 470))
        self.results_table = MyTable(self.results_tab)
        self.results_table.setGeometry(QtCore.QRect(0, 0, 400, 415))
        self.results_table.setSortingEnabled(False)
        self.results_table.setModel(PandasModel(pd.DataFrame(results)))
        self.results_table.setColumnWidth(0, 250)

        self.df = pd.DataFrame(z_score)
        self.df.name = 'z-score'

        self.z_score_tab = QtWidgets.QWidget(self)
        self.z_score_tab.setGeometry(QtCore.QRect(0, 0, 901, 470))
        z_chart = LineChart(self.z_score_tab, self.df)
        z_chart.setGeometry(QtCore.QRect(0, 0, 880, 420))

        self.pushButton_40 = QtWidgets.QPushButton(self)
        self.pushButton_40.setGeometry(QtCore.QRect(810, 0, 71, 31))
        self.pushButton_40.setObjectName("pushButton_40")
        self.pushButton_40.setText("close")

        #self.button2 = QtWidgets.QPushButton(self.results)
        #self.button2.setGeometry(QtCore.QRect(10, 410, 80, 60))
        #self.button2.setText("save result")

        self.addTab(self.logs_tab, "Backtest logs")
        self.addTab(self.results_tab, "Backtest results")
        self.addTab(self.z_score_tab, "z-score")

        #self.button2.clicked.connect(self.save_results)
        self.pushButton_40.clicked.connect(self.close_analysis)

    #closes tab
    def close_analysis(self):
        self.parenttabs.removeTab(self.parenttabs.currentIndex())

    # saves result to file
    def save_results(self):
        try:
            results = pd.read_csv('Backtests.csv', index=True)
            results.iloc[len(results)] = self.results
            results.to_csv('Backtests.csv')

        except FileNotFoundError:
            results = pd.DataFrame(columns=[self.results.index.values])
            results.iloc[0] = self.results
            results.to_csv('Backtests.csv')



# window with stationarity test results
class TestWindow(QtWidgets.QWidget):
    def __init__(self, df):
        super().__init__()

        self.setGeometry(QtCore.QRect(0, 0, 200+120*len(df.columns), 100))
        self.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"Ubuntu Bold\";")

        self.table = MyTable(self)
        self.table.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Ubuntu Condensed\";")

        self.table.setGeometry(QtCore.QRect(0, 0, 200+120*len(df.columns), 100))
        self.table.setModel(PandasModel(df))
        base_columns = [col for col in df.columns if '_' not in col and 'H0' not in col]
        for i in range(len(df.columns)-len(base_columns)):
            if i == 0:
                self.table.setColumnWidth(i, 210)
            else:
                self.table.setColumnWidth(i+len(base_columns), 120)

        self.show()


# Tabwidget with Johansen test results
class JohansenTabs(QtWidgets.QTabWidget):
    def __init__(self, parent, zaur, test, coins, index):
        super().__init__(parent)

        self.zaur = zaur
        self.parenttabs = parent
        self.setGeometry(QtCore.QRect(0, 10, 901, 500))
        self.setStyleSheet("background-color: rgb(6, 12, 26);\n"
                           "alternate-background-color: rgb(2, 26, 36);\n"
                           "selection-background-color: rgb(2, 36, 16);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 14pt \"Ubuntu Condensed\";")



        self.test_tab = QtWidgets.QWidget(self)
        self.test_tab.setGeometry(QtCore.QRect(0, 0, 901, 470))
        print(pd.DataFrame(test.r0t))
        spread = pd.DataFrame(data=test.r0t, index=index[:len(test.r0t)])
        spread.name = 'spread'
        self.resid_tab1 = LineChart(self, spread)
        self.resid_tab1.setGeometry(QtCore.QRect(0, 0, 901, 470))


        z_score = (spread-spread.mean())/spread.std()
        z_score.name = 'z_score'
        self.resid_z_score = LineChart(self, z_score)
        self.resid_z_score.setGeometry(QtCore.QRect(0, 0, 901, 470))



        eig_label = QtWidgets.QLabel(self.test_tab)
        eig_label.setGeometry(QtCore.QRect(10, 10, 200, 30))
        eig_label.setText('Maximum eigenvalue test')
        eig_table = MyTable(self.test_tab)
        eig_table.setSortingEnabled(False)

        eig_table.setGeometry(QtCore.QRect(10, 50, 500, 220))
        eig_df = pd.DataFrame({'test stat': np.round(test.max_eig_stat, 3)})
        eig_table.setModel(PandasModel(eig_df))


        trace_label = QtWidgets.QLabel(self.test_tab)
        trace_label.setGeometry(QtCore.QRect(480, 10, 200, 30))
        trace_label.setText('Trace test')
        trace_table = MyTable(self.test_tab)
        trace_table.setSortingEnabled(False)

        trace_table.setGeometry(QtCore.QRect(460, 50, 440, 220))
        trace_df = pd.DataFrame({'trace stat': np.round(test.lr1, 3)})
        trace_df[['10%', '5%', '1%']] = test.trace_stat_crit_vals
        trace_df.index = trace_df.index.map(lambda x: 'r=0' if x == 0 else f'r<={x}')
        trace_table.setModel(PandasModel(trace_df))

        eigenvector_label = QtWidgets.QLabel(self.test_tab)
        eigenvector_label.setGeometry(QtCore.QRect(10, 210, 200, 30))
        eigenvector_label.setText('Eigenvectors')

        self.eigenvector_table = MyTable(self.test_tab)
        self.eigenvector_table.setSortingEnabled(False)
        self.eigenvector_table.setGeometry(QtCore.QRect(10, 250, 500, 220))
        self.eigenvector_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)

        self.eigen_vectors = pd.DataFrame(data=np.round(test.evec, 6), columns=range(len(coins)), index=coins)

        self.eigenvector_table.setModel(PandasModel(self.eigen_vectors))

        eigenvalues_label = QtWidgets.QLabel(self.test_tab)
        eigenvalues_label.setGeometry(QtCore.QRect(460, 210, 200, 30))
        eigenvalues_label.setText('Eigenvalues')
        eigenvalues_table = MyTable(self.test_tab)

        eigenvalues_table.setGeometry(QtCore.QRect(460, 250, 440, 220))
        eigenvalues_df = pd.DataFrame(test.eig.round(5))
        eigenvalues_table.setModel(PandasModel(eigenvalues_df))

        eig_df[['10%', '5%', '1%']] = test.max_eig_stat_crit_vals
        eig_df.index = eig_df.index.map(lambda x: 'r=0' if x == 0 else f'r<={x}')
        eig_table.setModel(PandasModel(eig_df))


        self.pushButton_40 = QtWidgets.QPushButton(self)
        self.pushButton_40.setGeometry(QtCore.QRect(810, 0, 71, 31))
        self.pushButton_40.setObjectName("pushButton_40")
        self.pushButton_40.setText("close")



        #self.button2 = QtWidgets.QPushButton(self.stats_tab)
        #self.button2.setGeometry(QtCore.QRect(10, 410, 80, 60))
        #self.button2.setText("save result")

        self.addTab(self.test_tab, "Johansen test")
        self.addTab(self.resid_tab1, "Residuals for ΔY")
        self.addTab(self.resid_z_score, "Z-score")

        #self.button2.clicked.connect(self.save_results)
        self.pushButton_40.clicked.connect(self.close_analysis)



    # close tab
    def close_analysis(self):
        self.parenttabs.removeTab(self.parenttabs.currentIndex())

    # saves results to file
    def save_results(self):
        try:
            results = pd.read_csv('Johansen_tests.csv', index=True)
            results.iloc[len(results)] = self.results
            results.to_csv('Johansen_tests.csv')

        except FileNotFoundError:
            results = pd.DataFrame(columns=[self.results.index.values])
            results.iloc[0] = self.results
            results.to_csv('EG_tests.csv')




