import pymysql
import sqlite3

from typing import Union


class OpenPySQL:

    def __init__(self, connection: object, engine: str):
        self.con = connection
        self.eng = engine
        match self.eng:
            case 'sqlite':
                self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    @classmethod
    def sqlite(cls, filepath: str):
        connection = sqlite3.connect(filepath)
        return cls(connection, 'sqlite')

    @classmethod
    def mysql(cls, user: str, password: str, database: str, host: str = 'localhost', port: int = 3306):
        connection = pymysql.connect(host=host,
                                     port=port,
                                     user=user,
                                     password=password,
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        return cls(connection, 'mysql')

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query: str):
        match self.eng:
            case 'mysql':
                query = query.replace('?', '%s')
        self._query = query

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Union[int, str, list, tuple, None]):
        if value:
            if any(isinstance(value, t) for t in [int, str]):
                value = (value,)
            if isinstance(value, list):
                value = tuple(value)
        self._value = value or ()

    def fetch(self, size: int = 1) -> Union[list, dict, None]:
        match self.eng:
            case 'mysql':
                self.cur.execute(self.query, self.value)
                match size:
                    case 0:
                        return self.cur.fetchall()
                    case 1:
                        return self.cur.fetchone()
            case 'sqlite':
                exe = self.cur.execute(self.query, self.value)
                match size:
                    case 0:
                        if res := exe.fetchall():
                            return [{k: r[k] for k in r.keys()} for r in res]
                    case 1:
                        if res := exe.fetchone():
                            return {k: res[k] for k in res.keys()}
        return

    def execute(self) -> None:
        if self.value:
            if any(isinstance(self.value[0], t) for t in [str, int]):
                self.cur.execute(self.query, self.value)
            else:
                self.cur.executemany(self.query, self.value)
        else:
            self.cur.execute(self.query, self.value)
        self.con.commit()

    def close(self) -> None:
        self.con.close()
