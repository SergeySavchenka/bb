import pymysql
from db_config import *


class Database:
    def __init__(self):
        self.con = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DBNAME
        )
        self.cursor = self.con.cursor()

    def getDataFromTable(self, table_name):
        self.cursor.execute(f'select * from {table_name}')
        return self.cursor.fetchall()

    def getTables(self):
        self.cursor.execute('show tables')
        return [x for (x, ) in self.cursor.fetchall()]

    def describeTable(self, table_name):
        self.cursor.execute(f'describe {table_name}')
        return [x[0] for x in self.cursor.fetchall()]

    def updateDB(self, table_name, id_column, id_data, cell_column, cell_data):
        try:
            self.cursor.execute(f"update {table_name} set {cell_column} = '{cell_data}' "
                                f"where {id_column} = {id_data}")
            self.con.commit()
        except Exception:
            return 'Проверьте тип введенных данных'

    def delRecord(self, table_name, id_column, id_data):
        self.cursor.execute(f"delete from {table_name} where {id_column} = {id_data}")
        self.con.commit()
