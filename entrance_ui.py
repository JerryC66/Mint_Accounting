# Form implementation generated from reading ui file 'entrance.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_loginDlg(object):
    def setupUi(self, loginDlg):
        loginDlg.setObjectName("loginDlg")
        loginDlg.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        loginDlg.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=loginDlg)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 941, 591))
        self.centralwidget.setObjectName("centralwidget")
        self.Login = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Login.setGeometry(QtCore.QRect(240, 420, 91, 31))
        font = QtGui.QFont()
        font.setFamily("System")
        font.setBold(True)
        self.Login.setFont(font)
        self.Login.setObjectName("Login")
        self.Register = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Register.setGeometry(QtCore.QRect(430, 420, 91, 31))
        font = QtGui.QFont()
        font.setFamily("System")
        font.setBold(True)
        self.Register.setFont(font)
        self.Register.setObjectName("Register")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 70, 311, 121))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(220, 250, 120, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(220, 320, 120, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.Quit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Quit.setGeometry(QtCore.QRect(630, 490, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        self.Quit.setFont(font)
        self.Quit.setObjectName("Quit")
        self.Inputusername = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Inputusername.setGeometry(QtCore.QRect(390, 240, 211, 41))
        self.Inputusername.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Inputusername.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.LogicalMoveStyle)
        self.Inputusername.setObjectName("Inputusername")
        self.Inputpassword = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Inputpassword.setGeometry(QtCore.QRect(390, 310, 211, 41))
        self.Inputpassword.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Inputpassword.setObjectName("Inputpassword")
        self.menubar = QtWidgets.QMenuBar(parent=loginDlg)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuEntrance = QtWidgets.QMenu(parent=self.menubar)
        self.menuEntrance.setObjectName("menuEntrance")
        self.statusbar = QtWidgets.QStatusBar(parent=loginDlg)
        self.statusbar.setGeometry(QtCore.QRect(0, 0, 3, 20))
        self.statusbar.setObjectName("statusbar")
        self.menubar.addAction(self.menuEntrance.menuAction())

        self.retranslateUi(loginDlg)
        QtCore.QMetaObject.connectSlotsByName(loginDlg)

    def retranslateUi(self, loginDlg):
        _translate = QtCore.QCoreApplication.translate
        loginDlg.setWindowTitle(_translate("loginDlg", "MainWindow"))
        self.Login.setText(_translate("loginDlg", "Log in"))
        self.Register.setText(_translate("loginDlg", "Register"))
        self.label.setText(_translate("loginDlg", "WELCOME!"))
        self.groupBox.setTitle(_translate("loginDlg", "Username:"))
        self.groupBox_2.setTitle(_translate("loginDlg", "Password:"))
        self.Quit.setText(_translate("loginDlg", "Quit"))
        self.Inputusername.setPlaceholderText(_translate("loginDlg", "Please input your username~"))
        self.Inputpassword.setPlaceholderText(_translate("loginDlg", "Please input your password~"))
        self.menuEntrance.setTitle(_translate("loginDlg", "Entrance"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loginDlg = QtWidgets.QDialog()
    ui = Ui_loginDlg()
    ui.setupUi(loginDlg)
    loginDlg.show()
    sys.exit(app.exec())
