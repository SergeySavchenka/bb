import sys

from db_file import Database
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem)
from form import *
from addForm import Ui_MainWindow as Ui_AddWindow
from authForm import Ui_MainWindow as Ui_AuthWindow
from addDialog import *


class MainApp(QMainWindow):
    def __init__(self, database, link, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = database
        self.par = link
        self.par.close()
        self.ui.tableComboBox.setPlaceholderText('Таблицы')
        self.populate_comboBox()
        self.ui.mainTableWidget.setSortingEnabled(True)
        self.ui.tableComboBox.currentTextChanged.connect(self.populate_table)
        self.ui.mainTableWidget.cellChanged.connect(self.updateData)
        self.ui.delButton.clicked.connect(self.delData)
        self.ui.addButton.clicked.connect(self.addData)
        self.ui.addEmpButton.clicked.connect(self.openDialog)

    def populate_table(self):
        self.ui.mainTableWidget.clearContents()

        table_data = self.db.getDataFromTable(self.ui.tableComboBox.currentText())
        table_labels = self.db.getTableLabels(self.ui.tableComboBox.currentText())

        self.ui.mainTableWidget.setRowCount(len(table_data))
        self.ui.mainTableWidget.setColumnCount(len(table_labels))
        self.ui.mainTableWidget.setHorizontalHeaderLabels(table_labels)
        self.ui.mainTableWidget.setColumnHidden(0, True)

        if table_data:
            self.ui.mainTableWidget.blockSignals(True)

            for row, row_data in enumerate(table_data):
                for column, data in enumerate(row_data):
                    self.ui.mainTableWidget.setItem(row, column, QTableWidgetItem(str(data)))
            self.ui.mainTableWidget.blockSignals(False)

        self.ui.mainTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.ui.mainTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def populate_comboBox(self):
        tables = self.db.getTables()
        self.ui.tableComboBox.clear()
        self.ui.tableComboBox.addItems(tables)
        if self.ui.tableComboBox.currentText():
            self.populate_table()

    def updateData(self, row, column):
        new_data = self.ui.mainTableWidget.item(row, column).text()
        data_column = self.ui.mainTableWidget.takeHorizontalHeaderItem(column).text()
        id_data = self.ui.mainTableWidget.item(row, 0).text()
        id_column = self.ui.mainTableWidget.takeHorizontalHeaderItem(0).text()
        table = self.ui.tableComboBox.currentText()
        error = self.db.updateDB(table, new_data, data_column, id_data, id_column)
        self.populate_table()
        if error:
            QMessageBox.warning(self, 'Внимание', error)

    def delData(self):
        try:

            if self.ui.tableComboBox.currentText():
                table_name = self.ui.tableComboBox.currentText()

                if self.ui.mainTableWidget.currentRow() >= 0:
                    row = self.ui.mainTableWidget.currentRow()
                    id_column = self.ui.mainTableWidget.takeHorizontalHeaderItem(0).text()
                    id_data = self.ui.mainTableWidget.item(row, 0).text()
                    confirm = QMessageBox.question(self, 'Подтвердите удаление данных',
                                                   'Вы действительно хотите удалить запись?',
                                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if confirm == QMessageBox.StandardButton.Yes:
                        self.db.delRecord(table_name, id_data, id_column)
                        QMessageBox.information(self, 'Внимание', 'Запись удалена')
                    self.populate_table()
                else:
                    QMessageBox.warning(self, 'Внимание', 'Выберите данные для удаления')
            else:
                QMessageBox.warning(self, 'Внимание', 'Выберите таблицу')

        except Exception as e:
            print(e)

    def addData(self):
        try:
            table_name = self.ui.tableComboBox.currentText()
            columns = self.db.getTableLabels(table_name) if self.ui.tableComboBox.currentText() else None

            if columns:
                add_window = AddDataWindow(self.db, self, table_name, columns, self)
                add_window.show()
            else:
                QMessageBox.warning(self, 'Внимание', 'Выберите таблицу')

            if self.ui.tableComboBox.currentText():
                self.populate_table()
        except Exception as e:
            print(e)

    def openDialog(self):
        try:
            dialog = QtWidgets.QDialog(self)
            ui = Ui_Dialog()
            ui.setupUi(dialog)
            dialog.show()
            ui.roleComboBox.setPlaceholderText('Роли')
            roles = self.db.getDataFromTable('roles')
            ui.roleComboBox.addItems([x[1] for x in roles])
            ui.addEmpButton.clicked.connect(lambda x: self.addEmployee(ui))
        except Exception as e:
            print(e)

    def addEmployee(self, ui):
        newEmpName = ui.nameLineEdit.text()
        newEmpLogin = ui.loginLineEdit.text()
        newEmpPassword = newEmpLogin + 'pass'
        newEmpRole = ui.roleComboBox.currentText() if ui.roleComboBox.currentText() else 0
        if newEmpName and newEmpLogin and newEmpPassword and newEmpRole:
            try:
                self.db.addNewEmployee(newEmpName, newEmpLogin, newEmpPassword, newEmpRole)
                QMessageBox.information(self, 'Внимание', 'Пользователь добавлен')
            except Exception as e:
                print(e)
        else:
            QMessageBox.warning(self, 'Внимание', 'Проверьте введенные данные')

    def closeEvent(self, a0):
        self.par.setVisible(True)
        self.par.ui.loginLineEdit.clear()
        self.par.ui.passwordLineEdit.clear()
        self.close()


class AddDataWindow(QMainWindow):
    def __init__(self, database, link, table_name=None, columns=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_AddWindow()
        self.ui.setupUi(self)
        self.columns = columns
        self.table_name = table_name
        self.db = database
        self.inputs = {}
        self.par = link
        self.ui.label.setText(f"Добавление данных в таблицу <{table_name}>")
        self.populate_GridLayout()
        self.ui.pushButton.clicked.connect(self.addToDB)

    def populate_GridLayout(self):
        for i, column_name in enumerate(self.columns[1:]):
            label = QLabel(column_name)
            textEdit = QLineEdit()
            self.ui.gridLayout.addWidget(label, i, 0)
            self.ui.gridLayout.addWidget(textEdit, i, 1)
            self.inputs[column_name] = textEdit

    def addToDB(self):
        try:
            data = {}
            for column, widget in self.inputs.items():
                if widget.text().strip():
                    data[column] = widget.text().strip()

            columns = data.keys()
            values = [x for x in data.values()]
            self.db.addRecord(self.table_name, columns, values)
            self.par.populate_table()
            self.close()
        except Exception as e:
            print(e)


class AuthorizationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AuthWindow()
        self.ui.setupUi(self)
        self.link = None
        self.ui.enterButton.clicked.connect(self.enter)
        self.db = Database()
        self.ui.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def receive_link(self, link):
        self.link = link

    def enter(self):
        login = self.ui.loginLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        if login and password:
            role_id = self.db.checkUser(login, password)
            if role_id:
                role_id = role_id[0]
                if role_id == 2:

                    main_win = MainApp(self.db, self.link, self)
                    main_win.show()
                    self.setVisible(False)
                    QMessageBox.information(self, 'Внимание', 'Успешный вход')
                else:
                    # main_user_win = UserMainApp(self.db, self.link, self)
                    # main_user_win.show()
                    # self.setVisible(False)
                    QMessageBox.information(self, 'Внимание', 'Открывается окно пользователя')
            else:
                QMessageBox.warning(self, 'Внимание', 'Проверьте введенные данные')
        else:
            QMessageBox.warning(self, 'Внимание', 'Введите логин и пароль')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AuthorizationWindow()
    window.receive_link(window)
    window.show()
    sys.exit(app.exec())
