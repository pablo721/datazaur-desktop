# Form implementation generated from reading ui file 'messenger.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1329, 820)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 5, 1281, 656))
        self.widget.setObjectName("widget")
        self.groupBox_12 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_12.setGeometry(QtCore.QRect(2, -2, 191, 176))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_12.setFont(font)
        self.groupBox_12.setObjectName("groupBox_12")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_2.setGeometry(QtCore.QRect(5, 25, 121, 22))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(8)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_37 = QtWidgets.QPushButton(self.groupBox_12)
        self.pushButton_37.setGeometry(QtCore.QRect(160, 150, 25, 19))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_37.setFont(font)
        self.pushButton_37.setObjectName("pushButton_37")
        self.pushButton_36 = QtWidgets.QPushButton(self.groupBox_12)
        self.pushButton_36.setGeometry(QtCore.QRect(5, 150, 66, 19))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_36.setFont(font)
        self.pushButton_36.setObjectName("pushButton_36")
        self.tableView_4 = QtWidgets.QTableView(self.groupBox_12)
        self.tableView_4.setGeometry(QtCore.QRect(5, 53, 181, 91))
        self.tableView_4.setObjectName("tableView_4")
        self.pushButton_38 = QtWidgets.QPushButton(self.groupBox_12)
        self.pushButton_38.setGeometry(QtCore.QRect(130, 150, 25, 19))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_38.setFont(font)
        self.pushButton_38.setObjectName("pushButton_38")
        self.pushButton_33 = QtWidgets.QPushButton(self.groupBox_12)
        self.pushButton_33.setGeometry(QtCore.QRect(135, 25, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_33.setFont(font)
        self.pushButton_33.setObjectName("pushButton_33")
        self.groupBox_5 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_5.setGeometry(QtCore.QRect(2, 355, 191, 181))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_5)
        self.layoutWidget.setGeometry(QtCore.QRect(6, 29, 181, 151))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout.addWidget(self.lineEdit_5)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout.addWidget(self.lineEdit_3)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout.addWidget(self.lineEdit_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pushButton_35 = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_35.setFont(font)
        self.pushButton_35.setCheckable(True)
        self.pushButton_35.setAutoExclusive(True)
        self.pushButton_35.setObjectName("pushButton_35")
        self.horizontalLayout.addWidget(self.pushButton_35)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox_10 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_10.setGeometry(QtCore.QRect(2, 172, 191, 186))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_10.setFont(font)
        self.groupBox_10.setObjectName("groupBox_10")
        self.tableView_3 = QtWidgets.QTableView(self.groupBox_10)
        self.tableView_3.setGeometry(QtCore.QRect(5, 27, 181, 131))
        self.tableView_3.setObjectName("tableView_3")
        self.pushButton_39 = QtWidgets.QPushButton(self.groupBox_10)
        self.pushButton_39.setGeometry(QtCore.QRect(115, 160, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_39.setFont(font)
        self.pushButton_39.setObjectName("pushButton_39")
        self.pushButton_43 = QtWidgets.QPushButton(self.groupBox_10)
        self.pushButton_43.setGeometry(QtCore.QRect(5, 160, 66, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_43.setFont(font)
        self.pushButton_43.setObjectName("pushButton_43")
        self.tabWidget_3 = QtWidgets.QTabWidget(self.widget)
        self.tabWidget_3.setGeometry(QtCore.QRect(197, 5, 1087, 641))
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_8)
        self.scrollArea.setGeometry(QtCore.QRect(-1, 0, 1085, 611))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1083, 609))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setGeometry(QtCore.QRect(0, -1, 1081, 611))
        self.textEdit.setObjectName("textEdit")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget_3.addTab(self.tab_8, "")
        self.groupBox_11 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_11.setGeometry(QtCore.QRect(5, 535, 190, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_11.setFont(font)
        self.groupBox_11.setObjectName("groupBox_11")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_11)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_40 = QtWidgets.QPushButton(self.groupBox_11)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_40.setFont(font)
        self.pushButton_40.setCheckable(True)
        self.pushButton_40.setAutoExclusive(True)
        self.pushButton_40.setObjectName("pushButton_40")
        self.gridLayout_3.addWidget(self.pushButton_40, 0, 0, 1, 1)
        self.pushButton_44 = QtWidgets.QPushButton(self.groupBox_11)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_44.setFont(font)
        self.pushButton_44.setCheckable(True)
        self.pushButton_44.setAutoExclusive(True)
        self.pushButton_44.setObjectName("pushButton_44")
        self.gridLayout_3.addWidget(self.pushButton_44, 0, 1, 1, 1)
        self.pushButton_45 = QtWidgets.QPushButton(self.groupBox_11)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_45.setFont(font)
        self.pushButton_45.setCheckable(True)
        self.pushButton_45.setAutoExclusive(True)
        self.pushButton_45.setObjectName("pushButton_45")
        self.gridLayout_3.addWidget(self.pushButton_45, 1, 0, 1, 1)
        self.pushButton_41 = QtWidgets.QPushButton(self.groupBox_11)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_41.setFont(font)
        self.pushButton_41.setCheckable(True)
        self.pushButton_41.setAutoExclusive(True)
        self.pushButton_41.setObjectName("pushButton_41")
        self.gridLayout_3.addWidget(self.pushButton_41, 1, 1, 1, 1)
        self.pushButton_46 = QtWidgets.QPushButton(self.groupBox_11)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_46.setFont(font)
        self.pushButton_46.setCheckable(True)
        self.pushButton_46.setAutoExclusive(True)
        self.pushButton_46.setObjectName("pushButton_46")
        self.gridLayout_3.addWidget(self.pushButton_46, 2, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget_3.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_12.setTitle(_translate("Form", " search"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Username/email"))
        self.pushButton_37.setText(_translate("Form", "+"))
        self.pushButton_36.setText(_translate("Form", "clear"))
        self.pushButton_38.setText(_translate("Form", "-"))
        self.pushButton_33.setText(_translate("Form", "find"))
        self.groupBox_5.setTitle(_translate("Form", " create"))
        self.lineEdit_5.setPlaceholderText(_translate("Form", "name..."))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "password..."))
        self.lineEdit_4.setPlaceholderText(_translate("Form", "description"))
        self.label.setText(_translate("Form", "max guests"))
        self.comboBox.setItemText(0, _translate("Form", "room"))
        self.comboBox.setItemText(1, _translate("Form", "channel"))
        self.pushButton_35.setText(_translate("Form", "create!"))
        self.groupBox_10.setTitle(_translate("Form", "   friends"))
        self.pushButton_39.setText(_translate("Form", "msg"))
        self.pushButton_43.setText(_translate("Form", "import"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_8), _translate("Form", "Public ZaurRoom"))
        self.groupBox_11.setTitle(_translate("Form", " share"))
        self.pushButton_40.setText(_translate("Form", "trade"))
        self.pushButton_44.setText(_translate("Form", "post"))
        self.pushButton_45.setText(_translate("Form", "idea"))
        self.pushButton_41.setText(_translate("Form", "event"))
        self.pushButton_46.setText(_translate("Form", "news"))
