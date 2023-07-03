import sqlite3
from user import User
from db_conn import execute_on_database, create_connection, get_data_from_database


def test_add_user_to_database_positive():
    create_table_query = """DROP TABLE IF EXISTS users;

        CREATE TABLE IF NOT EXISTS users (
            user_id	INTEGER	PRIMARY KEY	AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email_address TEXT NOT NULL
        );
    """
    i_first_name = "Schuyler"
    i_last_name = "O'Hara"
    i_email_address = "Wilfrid17@yahoo.com"
    get_query = """SELECT * FROM users"""

    with sqlite3.connect(':memory:') as connection:
        conn = connection
        execute_on_database(conn, create_table_query)
        User.add_user(conn, i_first_name, i_last_name, i_email_address)
        data = get_data_from_database(conn, get_query)

    for user in data:
        user_id, first_name, last_name, email_address = user
        r_user_id = user_id
        r_first_name = first_name
        r_last_name = last_name
        r_email_address = email_address

    assert r_user_id == 1
    assert r_first_name == i_first_name
    assert r_last_name == i_last_name
    assert r_email_address == i_email_address


def test_add_user_to_database_negative():
    create_table_query = """DROP TABLE IF EXISTS users;

        CREATE TABLE IF NOT EXISTS users (
            user_id	INTEGER	PRIMARY KEY	AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email_address TEXT NOT NULL
        );
    """
    i_first_name = "Schuyler"
    i_last_name = "O'Hara"
    i_email_address = "Wilfrid17@yahoo.com"
    get_query = """SELECT * FROM users"""

    with sqlite3.connect(':memory:') as connection:
        conn = connection
        execute_on_database(conn, create_table_query)
        User.add_user(conn, i_first_name, 'Hartmann', i_email_address)
        data = get_data_from_database(conn, get_query)

    for user in data:
        user_id, first_name, last_name, email_address = user
        r_user_id = user_id
        r_first_name = first_name
        r_last_name = last_name
        r_email_address = email_address

    assert r_user_id not in range(2, 11)
    assert r_first_name == i_first_name
    assert r_last_name != i_last_name
    assert r_email_address == i_email_address
