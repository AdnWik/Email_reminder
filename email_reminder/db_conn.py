import sqlite3


DATABASE_NAME = 'base.db'

def create_connection():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
    return cur


def insert_into_database(query, data):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        cur.executemany(query, data)
        conn.commit()
