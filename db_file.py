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

    def getTables(self):
        self.cursor.execute('show tables')
        return [x for (x, ) in self.cursor.fetchall()]

    def getDataFromTable(self, table_name):
        self.cursor.execute(f'select * from {table_name}')
        return self.cursor.fetchall()

    def getTableLabels(self, table_name):
        self.cursor.execute(f'describe {table_name}')
        return [x[0] for x in self.cursor.fetchall()]

    def updateDB(self, table, new_data, data_column, id_data, id_column):
        self.cursor.execute(f"update {table} set {data_column} = '{new_data}' "
                            f"where {id_column} = {id_data}")
        self.con.commit()

    def delRecord(self, table, record_id, id_column):
        self.cursor.execute(f"DELETE FROM {table} WHERE {id_column} = {record_id}")
        self.con.commit()

    def addRecord(self, table_name, columns, values):
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))

        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.con.commit()

    def checkUser(self, login, password):
        self.cursor.execute(f"select roles.id from employees "
                            f"inner join roles on roles.id = employees.role_id "
                            f"where login = %s and password = %s", (login, password))
        role_id = self.cursor.fetchall()

        return [x for (x, ) in role_id]

    def addNewEmployee(self, name, login, password, role):
        self.cursor.execute(f"insert into employees(name, login, password, role_id) "
                            f"values(%s, %s, %s, (select id from roles "
                            f"where role_name = %s))", (name, login, password, role))
        self.con.commit()

