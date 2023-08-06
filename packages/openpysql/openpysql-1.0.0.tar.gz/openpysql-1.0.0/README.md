# OpenPySQL

[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![Python package](https://github.com/joumaico/openpysql/actions/workflows/python-package.yml/badge.svg)](https://github.com/joumaico/openpysql/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/joumaico/openpysql/actions/workflows/python-publish.yml/badge.svg)](https://github.com/joumaico/openpysql/actions/workflows/python-publish.yml)

Lightweight interface for accessing MySQL and SQLite database.

## Installation

```console
$ pip install openpysql
```

## Modules

### *class* openpysql.OpenPySQL()

#### *classmethod* .sqlite(filepath)
↳ Connection is open for SQLite database.
```python
from openpysql import OpenPySQL

db = OpenPySQL.sqlite('test.db')
```

#### *classmethod* .mysql(user, password, database, host='localhost', port=3306)
↳ Connection is open for MySQL database.
```python
from openpysql import OpenPySQL

db = OpenPySQL.mysql(user='user', password='password', database='test')
```

#### *property* .query(str)
↳ Query to execute, a question mark `?` can be used as a placeholder in the query.
```python
db.query = "SELECT * FROM students WHERE gender=?;"
```

#### *property* .value(Union[int, str, list, tuple, None])
↳ Parameters used with query.
```python
db.value = 'M'
```

#### .execute() -> None
↳ Execute a query.
```python
db.query = "INSERT INTO students (first_name, last_name, gender) VALUES (?, ?, ?);"
db.value = ('Eloise', 'Robinson', 'F')
db.execute()
```
```python
db.query = "INSERT INTO students (first_name, last_name, gender) VALUES (?, ?, ?);"
db.value = [('Jakob', 'Bryant', 'M'), ('Hannah', 'Mcgee', 'F')]
db.execute()
```

#### .fetch(size=1) -> Union[list, dict, None]
↳ Fetch row(s).
```python
db.query = "SELECT * FROM students WHERE gender=?;"
db.value = 'M'
db.fetch(0) # fetch all the rows.
db.fetch(1) # fetch the next row.
```

#### .close() -> None
↳ Send the quit message and close the socket.
```python
db.close()
```

## Links
* PyPI Releases: https://pypi.org/project/openpysql
* Source Code: https://github.com/joumaico/openpysql
