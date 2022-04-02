# -*- coding: utf-8 -*-

# Form implementation generated from reading views file 'login_screen.views'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from frontend import Frontzaur
from new_acc import AccountCreator

class LoginScreen(QtWidgets.QWidget):
    def __init__(self, zaur):
        super().__init__()
        self.zaur = zaur
        self.resize(308, 318)
        self.setStyleSheet("background-color: rgb(12, 28, 48);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 11pt \"FreeMono Bold\";")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 291, 301))
        font = QtGui.QFont()
        font.setFamily("FreeMono Bold")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.lineEdit_35 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_35.setGeometry(QtCore.QRect(10, 70, 271, 31))
        self.lineEdit_35.setInputMask("")
        self.lineEdit_35.setFrame(True)
        self.lineEdit_35.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.lineEdit_35.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                           "alternate-background-color: rgb(9, 21, 32); \n"
                           "color: rgb(255, 255, 255); \n"
                           "font: 50  10pt \"FreeMono Bold\";")
        self.lineEdit_36 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_36.setGeometry(QtCore.QRect(10, 140, 271, 31))
        self.lineEdit_36.setInputMask("")
        self.lineEdit_36.setFrame(True)
        self.lineEdit_36.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.lineEdit_36.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                           "alternate-background-color: rgb(9, 21, 32); \n"
                           "color: rgb(255, 255, 255); \n"
                           "font: 50  10pt \"FreeMono Bold\";")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 111, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 111, 17))
        self.label_2.setObjectName("label_2")
        self.pushButton_33 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_33.setGeometry(QtCore.QRect(160, 190, 121, 41))
        self.pushButton_33.setObjectName("pushButton_33")
        self.pushButton_34 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_34.setGeometry(QtCore.QRect(10, 190, 121, 41))
        self.pushButton_34.setObjectName("pushButton_34")
        self.pushButton_35 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_35.setGeometry(QtCore.QRect(160, 250, 121, 41))
        self.pushButton_35.setObjectName("pushButton_35")


        self.retranslateUi()

        self.pushButton_33.clicked.connect(self.login)
        self.pushButton_34.clicked.connect(self.new_account)
        self.pushButton_35.clicked.connect(self.close)

        QtCore.QMetaObject.connectSlotsByName(self)

    # checks password against hash and logs in
    def login(self):
        user = self.lineEdit_35.text().lower()
        password = self.lineEdit_36.text()

        if self.zaur.check_hash(user, password):
            self.zaur.login(user, password)
            ui = Frontzaur(self.zaur, user)
            ui.show()
            self.close()

        else:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('Wrong username or password. Try again.')




    # opens account creator
    def new_account(self):

        self.resize(313, 427)
        acc = AccountCreator(self, self.zaur)
        acc.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Login"))
        self.groupBox.setTitle(_translate("Form", " Datazaur"))
        self.label.setText(_translate("Form", "login"))
        self.label_2.setText(_translate("Form", "password"))
        self.pushButton_33.setText(_translate("Form", "log in"))
        self.pushButton_34.setText(_translate("Form", "new account"))
        self.pushButton_35.setText(_translate("Form", "exit"))


