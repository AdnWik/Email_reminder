from os import getenv
import sqlite3
from dotenv import load_dotenv


load_dotenv()


class Database:
    """Database context manager"""

    def __init__(self, connection) -> None:
        self.connection = connection
        self.cursor = None

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()

        self.connection.close()


DATABASE_NAME = getenv('DB_NAME')


def execute_on_database(script, db_name=DATABASE_NAME):
    connection = sqlite3.connect(db_name)
    with Database(connection) as database:
        database.cursor.executescript(script)


def insert_into_database(query, data):
    connection = sqlite3.connect(DATABASE_NAME)
    with Database(connection) as database:
        database.cursor.executemany(query, data)


def get_data_from_database(query):
    connection = sqlite3.connect(DATABASE_NAME)
    with Database(connection) as database:
        database.cursor.execute(query)
        return database.cursor.fetchall()
