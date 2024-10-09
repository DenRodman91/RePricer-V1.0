import pandas as pd
import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect('db/'+db_name+'.db')
        self.cursor = self.connection.cursor()

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()

    def execute(self, query, params=None):
        """Выполняет SQL запрос с параметрами."""
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self.cursor

    def commit(self):
        """Фиксирует изменения в базе данных."""
        self.connection.commit()

    def select(self, table, columns = False, condition=None, params=None):
        """Выполняет SELECT запрос."""
        query = f"SELECT {','.join(columns) if columns else '*'} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        result = self.execute(query, params).fetchall()
        return result

    def insert(self, table, columns, values, replace=False):
        """Выполняет INSERT запрос."""
        if not isinstance(values, list):
            values = [values]
        if replace:
            query = f"INSERT OR REPLACE INTO {table} ({', '.join(columns)}) VALUES ({','.join(['?']  *  len(columns))})"
        else:
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({','.join(['?']  *  len(columns))})"
        self.execute(query, values)
        self.commit()

    def update(self, table, set_columns:list, condition:str = None, params=None):
        """Выполняет UPDATE запрос."""
        query = f"UPDATE {table} SET {', '.join([f'{col}=?' for col in set_columns])}" + f" WHERE {condition}" if condition else ""
        self.execute(query, params)
        self.commit()

    def delete(self, table, condition, params):
        """Выполняет DELETE запрос."""
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute(query, params)
        self.commit()

    def to_dataframe(self, table, columns = False, condition=None, params=None):
        """Преобразует результаты SELECT запроса в pandas.DataFrame."""
        results = self.select(table, columns, condition, params)
        column_names = columns if columns else ["column%d" % i for i in range(1, len(results[0]) + 1)]
        df = pd.DataFrame(results, columns=column_names)
        return df
