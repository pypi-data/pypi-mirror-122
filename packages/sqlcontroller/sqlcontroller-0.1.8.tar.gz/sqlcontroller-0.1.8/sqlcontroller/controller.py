"""Facilitate handling a SQL database"""

import sqlite3
from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional
from sqlcontroller.validator import AbstractValidator, SqliteValidator
from sqlcontroller.querybuilder import SqliteQueryBuilder
from sqlcontroller.table import DbTable, SqliteTable
from sqlcontroller.field import Field

IterOpt = Optional[Iterable]
IterIterOpt = Optional[Iterable[Iterable]]


class NonExistentTableError(Exception):
    """Error for trying to retrieve a non-existent table"""


class AbstractSqlController(ABC):  # pragma: no cover
    """Abstract controller"""

    database: str
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor
    validator: AbstractValidator

    @abstractmethod
    def __enter__(self) -> "AbstractSqlController":
        """Enter controller context"""

    @abstractmethod
    def __exit__(self, *_) -> None:
        """Exit controller context"""

    @abstractmethod
    def connect_db(self) -> None:
        """Connect to a database"""

    @abstractmethod
    def disconnect_db(self) -> None:
        """Disconnect from a database"""

    @abstractmethod
    def save_db(self) -> None:
        """Save changes to a database"""

    @abstractmethod
    def set_cursor(self) -> None:
        """Get database cursor"""

    @abstractmethod
    def execute(
        self, query: str, table: str = None, values: IterOpt = None
    ) -> sqlite3.Cursor:
        """Execute sql query with one value set"""

    @abstractmethod
    def executemany(
        self,
        query: str,
        table: str = None,
        valuesets: IterIterOpt = None,
    ) -> sqlite3.Cursor:
        """Execute sql query with many value sets"""

    @abstractmethod
    def create_table(self, name: str, fields: Iterable[Field]) -> DbTable:
        """Add new table to a database"""

    @abstractmethod
    def get_table(self, name: str) -> DbTable:
        """Retrieve existing table"""

    @abstractmethod
    def delete_table(self, name: str) -> None:
        """Remove a table from a database"""


class BaseSqlController(AbstractSqlController):
    """Provide generic functionality for an SQL controller"""

    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, database):
        self.database = database

    def __enter__(self) -> "BaseSqlController":
        self.connect_db()
        return self

    def __exit__(self, *_) -> None:
        self.save_db()
        self.disconnect_db()

    def execute(
        self, query: str, table: str = None, values: IterOpt = None
    ) -> sqlite3.Cursor:
        """Execute sql query with one value set"""
        values = values if values else []
        query = query.format(table=table)

        try:
            return self.cursor.execute(query, values)
        except sqlite3.Error as error:
            print(f"Error: execute {query}")
            raise error

    def executemany(
        self,
        query: str,
        table: str = None,
        valuesets: IterIterOpt = None,
    ) -> sqlite3.Cursor:
        """Execute sql query with many value sets"""
        valuesets = valuesets if valuesets else [[]]
        query = query.format(table=table)

        try:
            return self.cursor.executemany(query, valuesets)
        except sqlite3.Error as error:
            print(f"Error: executemany {query}")
            raise error


class SqliteController(BaseSqlController):
    """Provide methods for database, table and row handling"""

    validator: SqliteValidator = SqliteValidator()

    def connect_db(self) -> None:
        """Connect to a database (create if non-existent)"""
        self.connection = sqlite3.connect(self.database)
        self.connection.row_factory = sqlite3.Row

        self.set_cursor()

    def disconnect_db(self) -> None:
        """Clear database connection"""
        self.connection.close()
        del self.connection
        del self.cursor

    def save_db(self) -> None:
        """Save changes to a database"""
        self.connection.commit()

    def set_cursor(self) -> None:
        """Get database cursor"""
        self.cursor = self.connection.cursor()

    def has_table(self, name: str) -> bool:
        """Check if table exists"""
        try:
            self.execute("select * from {table} limit 1", name)
            return True
        except sqlite3.OperationalError:
            return False

    def create_table(self, name: str, fields: Iterable[Field]) -> SqliteTable:
        """Create a new table"""

        self.validator.validate_table_params(name, fields)

        query = SqliteQueryBuilder.build_table_create_query(fields)
        self.execute(query, name)
        return SqliteTable(name, self)

    def get_table(self, name: str) -> SqliteTable:
        """Retrieve existing table"""
        self.validator.validate_table_name(name)

        if not self.has_table(name):
            raise NonExistentTableError(f"{name} table does not exist")

        return SqliteTable(name, self)

    def delete_table(self, name: str) -> None:
        """Delete table"""
        query = "drop table {table};"
        self.execute(query, name)

    @staticmethod
    def build_query_clauses(
        where: str = "", order: str = "", limit: int = 0, offset: int = 0
    ) -> str:
        """Build a query's clauses string"""
        return SqliteQueryBuilder.build_query_clauses(where, order, limit, offset)

    def fetchone(self) -> Any:
        """Get first select query result"""
        return self.cursor.fetchone()

    def fetchall(self) -> list:
        """Get all select query results"""
        return self.cursor.fetchall()
