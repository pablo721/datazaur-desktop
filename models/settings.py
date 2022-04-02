# -*- coding: utf-8 -*-

# Form implementation generated from reading views file 'tests_settings66.views'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class TestSettings(QtWidgets.QWidget):
    def __init__(self, zaur):
        super().__init__()
        self.zaur = zaur
        self.setObjectName("Form")
        self.setStyleSheet("background-color: rgb(6, 16, 36);\n"
                           "color: rgb(255, 255, 255);\n"
                           "font: 75 10pt \"Ubuntu Bold\";")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 251, 411))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 110, 231, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_17 = QtWidgets.QLabel(self.groupBox_2)
        self.label_17.setGeometry(QtCore.QRect(30, 30, 81, 21))
        self.label_17.setObjectName("label_17")
        self.comboBox_18 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_18.setGeometry(QtCore.QRect(130, 30, 91, 21))
        self.comboBox_18.setObjectName("comboBox_18")
        self.comboBox_18.addItem("")
        self.comboBox_18.addItem("")
        self.comboBox_18.addItem("")
        self.comboBox_18.addItem("")
        self.comboBox_19 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_19.setGeometry(QtCore.QRect(130, 60, 91, 21))
        self.comboBox_19.setObjectName("comboBox_19")
        self.comboBox_19.addItem("")
        self.comboBox_19.addItem("")
        self.comboBox_19.addItem("")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 90, 101, 21))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 60, 101, 21))
        self.radioButton_4.setChecked(True)
        self.radioButton_4.setAutoExclusive(True)
        self.radioButton_4.setObjectName("radioButton_4")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(130, 90, 91, 21))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 240, 231, 121))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_15 = QtWidgets.QLabel(self.groupBox_3)
        self.label_15.setGeometry(QtCore.QRect(30, 30, 81, 21))
        self.label_15.setObjectName("label_15")
        self.comboBox_10 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_10.setGeometry(QtCore.QRect(130, 30, 91, 21))
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_17 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_17.setGeometry(QtCore.QRect(130, 60, 91, 21))
        self.comboBox_17.setObjectName("comboBox_17")
        self.comboBox_17.addItem("")
        self.comboBox_17.addItem("")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton.setGeometry(QtCore.QRect(10, 60, 101, 21))
        self.radioButton.setChecked(True)
        self.radioButton.setAutoExclusive(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 90, 101, 21))
        self.radioButton_2.setObjectName("radioButton_2")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(130, 90, 91, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_32 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_32.setGeometry(QtCore.QRect(140, 370, 101, 31))
        self.pushButton_32.setObjectName("pushButton_32")
        self.pushButton_34 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_34.setGeometry(QtCore.QRect(10, 370, 101, 31))
        self.pushButton_34.setObjectName("pushButton_34")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 20, 231, 91))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_18 = QtWidgets.QLabel(self.groupBox_4)
        self.label_18.setGeometry(QtCore.QRect(10, 30, 81, 21))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.groupBox_4)
        self.label_19.setGeometry(QtCore.QRect(10, 60, 91, 21))
        self.label_19.setObjectName("label_19")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_7.setGeometry(QtCore.QRect(130, 60, 91, 21))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.comboBox_20 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_20.setGeometry(QtCore.QRect(130, 30, 91, 21))
        self.comboBox_20.setObjectName("comboBox_20")
        self.comboBox_20.addItem("")
        self.comboBox_20.addItem("")
        self.comboBox_20.addItem("")

        for line in [self.lineEdit_7, self.lineEdit_6, self.lineEdit_5]:
            line.setStyleSheet("background-color: rgb(12, 52, 82)\n;"
                               "color: rgb(255, 255, 255);")

        self.retranslateUi()
        self.default_config = {'adf_reg': 'c', 'kpss_reg': 'c', 'adf_autolag': 'AIC', 'kpss_autolag': 'auto'}

        self.options = {'adf_reg': {'const': 'c', 'const+trend': 'ct', 'const+linear+quadratic trend': 'ctt',
                                    'no const no trend': 'nc'},
                        'adf_autolag': {'AIC': 'AIC', 'BIC': 'BIC', 't-stat': 't-stat'},
                        'kpss_reg': {'const': 'c', 'const+trend': 'ct'},
                        'kpss_autolag': {'Hobijn': 'auto', 'Schwert': 'legacy'}}
        self.options_johansen = {'no deterministic terms': -1, 'constant term': 0, 'linear trend': 1}

        self.pushButton_32.clicked.connect(self.save_config)
        self.show()
        QtCore.QMetaObject.connectSlotsByName(self)

    def save_config(self):
        settings = {'adf_reg': self.options['adf_reg'][self.comboBox_18.currentText()],
                    'adf_autolag': self.options['adf_autolag'][self.comboBox_19.currentText()],
                    'kpss_reg': self.options['kpss_reg'][self.comboBox_10.currentText()],
                    'kpss_autolag': self.options['kpss_autolag'][self.comboBox_17.currentText()]}
        n_lags_johansen = int(self.lineEdit_7.text())

        det_order = self.options_johansen[self.comboBox_20.currentText()]
        settings_joh = {'det_order': det_order, 'n_lags': n_lags_johansen}

        print(settings)
        print(settings_joh)
        self.zaur.save_config(settings, settings_joh)
        dialog = QtWidgets.QMessageBox()
        dialog.setText('Settings saved.')
        dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                             "color: rgb(255, 255, 255);\n"
                             "font: 75 11pt \"FreeMono Bold\";")
        dialog.exec_()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "settings"))
        self.groupBox_2.setTitle(_translate("Form", "ADF"))
        self.label_17.setText(_translate("Form", "regression"))
        self.comboBox_18.setItemText(0, _translate("Form", "const"))
        self.comboBox_18.setItemText(1, _translate("Form", "const+trend"))
        self.comboBox_18.setItemText(2, _translate("Form", "const+linear+quadratic trend"))
        self.comboBox_18.setItemText(3, _translate("Form", "no const no trend"))
        self.comboBox_19.setItemText(0, _translate("Form", "AIC"))
        self.comboBox_19.setItemText(1, _translate("Form", "BIC"))
        self.comboBox_19.setItemText(2, _translate("Form", "t-stat"))
        self.radioButton_3.setText(_translate("Form", "manual lag"))
        self.radioButton_4.setText(_translate("Form", "lag method"))
        self.groupBox_3.setTitle(_translate("Form", "KPSS"))
        self.label_15.setText(_translate("Form", "regression"))
        self.comboBox_10.setItemText(0, _translate("Form", "const"))
        self.comboBox_10.setItemText(1, _translate("Form", "const+trend"))
        self.comboBox_17.setItemText(0, _translate("Form", "Hobijn"))
        self.comboBox_17.setItemText(1, _translate("Form", "Schwert"))
        self.radioButton.setText(_translate("Form", "lag method"))
        self.radioButton_2.setText(_translate("Form", "manual lag"))
        self.pushButton_32.setText(_translate("Form", "save"))
        self.pushButton_34.setText(_translate("Form", "reset"))
        self.groupBox_4.setTitle(_translate("Form", "Johansen"))
        self.label_18.setText(_translate("Form", "regression"))
        self.label_19.setText(_translate("Form", "lag number"))
        self.comboBox_20.setItemText(0, _translate("Form", "no deterministic terms"))
        self.comboBox_20.setItemText(1, _translate("Form", "constant term"))
        self.comboBox_20.setItemText(2, _translate("Form", "linear trend"))

