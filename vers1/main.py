import sys

from db_file import Database
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel, QLineEdit, QMessageBox
from form import Ui_MainWindow
from addForm import Ui_MainWindow as Ui_AddWindow


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()
        self.link = None
        self.ui.tableComboBox.setPlaceholderText('Таблицы')
        self.populate_comboBox()
        self.ui.mainTableWidget.setSortingEnabled(True)
        self.ui.tableComboBox.currentTextChanged.connect(self.populate_table)
        self.ui.mainTableWidget.cellChanged.connect(self.updateData)
        self.ui.delButton.clicked.connect(self.delData)
        self.ui.addButton.clicked.connect(self.addData)

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

        self.ui.mainTableWidget.resizeColumnsToContents()

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
        self.db.updateDB(table, new_data, data_column, id_data, id_column)
        self.populate_table()

    def delData(self):
        try:
            row = self.ui.mainTableWidget.currentRow()
            id_data = self.ui.mainTableWidget.item(row, 0).text()
            id_column = self.ui.mainTableWidget.takeHorizontalHeaderItem(0).text()
            self.db.delRecord(self.ui.tableComboBox.currentText(), id_data, id_column)
            self.populate_table()
        except Exception as e:
            QMessageBox.warning(self, 'Внимание', 'Выберите ячейку')

    def addData(self):
        table_name = self.ui.tableComboBox.currentText()
        columns = self.db.getTableLabels(table_name) if self.ui.tableComboBox.currentText() else None

        if columns:
            add_window = AddDataWindow(self.db, self.link, table_name, columns, self)
            add_window.show()
        else:
            QMessageBox.warning(self, 'Внимание', 'Выберите таблицу')

        if self.ui.tableComboBox.currentText():
            self.populate_table()

    def receive_link(self, link):
        self.link = link


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.receive_link(window)
    window.show()
    sys.exit(app.exec())
