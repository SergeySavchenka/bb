from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLabel, QLineEdit, QMessageBox, QHeaderView, QDialog, QVBoxLayout


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableComboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.tableComboBox.setObjectName("tableComboBox")
        self.horizontalLayout.addWidget(self.tableComboBox)
        self.addButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.delButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delButton.setObjectName("delButton")
        self.horizontalLayout.addWidget(self.delButton)
        self.addEmpButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addEmpButton.setObjectName("addEmpButton")
        self.horizontalLayout.addWidget(self.addEmpButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.mainTableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.mainTableWidget.setObjectName("mainTableWidget")
        self.mainTableWidget.setColumnCount(0)
        self.mainTableWidget.setRowCount(0)
        self.mainTableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.mainTableWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addButton.setText(_translate("MainWindow", "Добавить"))
        self.delButton.setText(_translate("MainWindow", "Удалить"))
        self.addEmpButton.setText(_translate("MainWindow", "Добавить сотрудника"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
