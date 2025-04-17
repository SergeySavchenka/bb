import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from mainForm import Ui_MainWindow
from db_file import Database


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()
        self.ui.tableComboBox.setPlaceholderText('Таблицы')
        self.populate_comBox()
        self.ui.tableComboBox.currentTextChanged.connect(self.populate_table)
        self.ui.mainTableWidget.cellChanged.connect(self.updateTable)
        self.ui.delButton.clicked.connect(self.delRecord)
        self.ui.addButton.clicked.connect(self.addRecord)

    def populate_comBox(self):
        tables = self.db.getTables()
        self.ui.tableComboBox.clear()
        self.ui.tableComboBox.addItems(tables)

    def populate_table(self):
        self.ui.mainTableWidget.clearContents()

        data = self.db.getDataFromTable(self.ui.tableComboBox.currentText())
        labels = self.db.describeTable(self.ui.tableComboBox.currentText())

        self.ui.mainTableWidget.setRowCount(len(data))
        self.ui.mainTableWidget.setColumnCount(len(labels))
        self.ui.mainTableWidget.verticalHeader().setVisible(False)
        self.ui.mainTableWidget.setHorizontalHeaderLabels(labels)
        self.ui.mainTableWidget.setColumnHidden(0, True)

        if data:
            self.ui.mainTableWidget.blockSignals(True)

            for row, row_data in enumerate(data):
                for column, column_data in enumerate(row_data):
                    self.ui.mainTableWidget.setItem(row, column, QTableWidgetItem(str(column_data)))
            self.ui.mainTableWidget.blockSignals(False)

            self.ui.mainTableWidget.resizeColumnsToContents()

    def addRecord(self):
        pass

    def updateTable(self, row, column):
        table = self.ui.tableComboBox.currentText()
        id_column = self.ui.mainTableWidget.takeHorizontalHeaderItem(0).text()
        id_data = self.ui.mainTableWidget.item(row, 0).text()
        cell_data = self.ui.mainTableWidget.item(row, column).text()
        cell_column = self.ui.mainTableWidget.takeHorizontalHeaderItem(column).text()
        error = self.db.updateDB(table, id_column, id_data, cell_column, cell_data)
        self.populate_table()
        if error:
            QMessageBox.warning(self, 'Внимание', error)

    def delRecord(self):
        try:
            if self.ui.tableComboBox.currentText():
                table_name = self.ui.tableComboBox.currentText()

                if self.ui.mainTableWidget.currentRow() >= 0:
                    row = self.ui.mainTableWidget.currentRow()
                    id_column = self.ui.mainTableWidget.takeHorizontalHeaderItem(0).text()
                    id_data = self.ui.mainTableWidget.item(row, 0).text()
                    self.db.delRecord(table_name, id_column, id_data)
                    self.populate_table()
                else:
                    QMessageBox.warning(self, 'Внимание', 'Выберите данные для удаления')
            else:
                QMessageBox.warning(self, 'Внимание', 'Выберите таблицу')
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())