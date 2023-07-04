import sqlite3


def create_connection():
    database_name = 'base.db'
    with sqlite3.connect(database_name) as conn:
        return conn


def execute_on_database(conn, script):
    cur = conn.cursor()
    cur.executescript(script)


def insert_into_database(conn, query, data):
    cur = conn.cursor()
    cur.executemany(query, data)
    conn.commit()


def get_data_from_database(conn, query):
    cur = conn.cursor()
    cur.execute(query)

    data = cur.fetchall()
    return data
