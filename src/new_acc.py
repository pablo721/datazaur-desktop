


from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser

class AccountCreator(QtWidgets.QWidget):
    def __init__(self, parent, zaur):
        super().__init__(parent)
        self.zaur = zaur
        self.parent = parent
        self.setObjectName("a")
        self.resize(313, 427)
        self.setStyleSheet("background-color: rgb(12, 28, 48);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 11pt \"FreeMono Bold\";")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 291, 401))
        font = QtGui.QFont()
        font.setFamily("FreeMono Bold")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.lineEdit_35 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_35.setGeometry(QtCore.QRect(10, 140, 271, 31))
        self.lineEdit_35.setInputMask("")
        self.lineEdit_35.setFrame(True)
        self.lineEdit_35.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.lineEdit_35.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                           "alternate-background-color: rgb(9, 21, 32); \n"
                           "color: rgb(255, 255, 255); \n"
                           "font: 50  10pt \"FreeMono Bold\";")
        self.lineEdit_36 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_36.setGeometry(QtCore.QRect(10, 70, 271, 31))
        self.lineEdit_36.setInputMask("")
        self.lineEdit_36.setFrame(True)
        self.lineEdit_36.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.lineEdit_36.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                           "alternate-background-color: rgb(9, 21, 32); \n"
                           "color: rgb(255, 255, 255); \n"
                           "font: 50  10pt \"FreeMono Bold\";")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 111, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 111, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 141, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_37 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_37.setGeometry(QtCore.QRect(10, 210, 271, 31))
        self.lineEdit_37.setInputMask("")
        self.lineEdit_37.setFrame(True)
        self.lineEdit_37.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_37.setObjectName("lineEdit_37")
        self.lineEdit_37.setStyleSheet("background-color: rgb(12, 52, 82);\n"
                           "alternate-background-color: rgb(9, 21, 32); \n"
                           "color: rgb(255, 255, 255); \n"
                           "font: 50  10pt \"FreeMono Bold\";")
        self.pushButton_33 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_33.setGeometry(QtCore.QRect(150, 290, 131, 41))
        self.pushButton_33.setObjectName("pushButton_33")
        self.pushButton_34 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_34.setGeometry(QtCore.QRect(10, 290, 131, 41))
        self.pushButton_34.setObjectName("pushButton_34")
        self.pushButton_35 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_35.setGeometry(QtCore.QRect(150, 350, 131, 41))
        self.pushButton_35.setObjectName("pushButton_35")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(10, 250, 201, 23))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi()



        self.pushButton_35.clicked.connect(self.go_back)
        self.pushButton_33.clicked.connect(self.create_account)
        self.pushButton_34.clicked.connect(self.read_license)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()


    # opens license page
    def read_license(self):
        webbrowser.open('https://github.com/bravetraveler74/Datazaur/blob/main/LICENSE')

    # goes back to login screen
    def go_back(self):
        self.parent.resize(308, 318)
        self.close()

    # creates new account
    def create_account(self):
        username = self.lineEdit_36.text().lower()
        pass1 = self.lineEdit_35.text()
        pass2 = self.lineEdit_37.text()

        query = f"SELECT user FROM users WHERE user='{username}'"
        usercheck = self.zaur.db.execute_read_query(query)

        print(usercheck)

        if usercheck:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Such user already exists.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            return

        elif not username:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Please input username.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()

        elif not pass1:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Please input password.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()

        elif (pass1 == pass2) and self.checkBox.checkState():
            self.zaur.add_hash(username, pass1)
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Account created successfully.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                "color: rgb(255, 255, 255);\n"
                                "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            self.parent.resize(308, 318)
            self.close()

        elif pass1 != pass2:
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Passwords do not match.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            return



        elif not self.checkBox.checkState():
            dialog = QtWidgets.QMessageBox()
            dialog.setText('Please accept terms of use.')
            dialog.setStyleSheet("background-color: rgb(12, 28, 48);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "font: 75 11pt \"FreeMono Bold\";")
            dialog.exec_()
            return

        else:
            return


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Create account"))
        self.groupBox.setTitle(_translate("Form", "   new account"))
        self.label.setText(_translate("Form", "login"))
        self.label_2.setText(_translate("Form", "password"))
        self.label_3.setText(_translate("Form", "confirm password"))
        self.pushButton_33.setText(_translate("Form", "create account"))
        self.pushButton_34.setText(_translate("Form", "terms of use"))
        self.pushButton_35.setText(_translate("Form", "back"))
        self.checkBox.setText(_translate("Form", "I accept terms of use."))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = AccountCreator()

    ui.show()
    sys.exit(app.exec_())
