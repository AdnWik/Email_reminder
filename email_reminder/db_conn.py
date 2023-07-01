import sqlite3


def create_connection():
    with sqlite3.connect('base.db') as conn:
        cur = conn.cursor()
    return cur