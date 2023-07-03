import sqlite3


DATABASE_NAME = 'base.db'


def create_connection():
    with sqlite3.connect(DATABASE_NAME) as conn:
        return conn


def execute_on_database(conn, query):
    cur = conn.cursor()
    cur.executescript(query)


def insert_into_database(conn, query, data):
    cur = conn.cursor()
    cur.executemany(query, data)
    conn.commit()


def get_data_from_database(conn, query):
    cur = conn.cursor()
    cur.execute(query)

    data = cur.fetchall()
    return data
