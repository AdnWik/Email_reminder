import sqlite3
from datetime import datetime
from rental import Rental
from db_conn import execute_on_database, get_data_from_database


def test_add_rental_to_database_positive():
    create_table_query = """DROP TABLE IF EXISTS rentals;

        CREATE TABLE IF NOT EXISTS rentals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            book_id     INTEGER NOT NULL,
            rental_date TEXT    NOT NULL,
            return_date TEXT    NOT NULL,
            returned    INTEGER
    );
    """
    i_user_id = 1
    i_book_id = 1
    rental_date_str = "2023-01-01 10:10:10"
    i_rental_date =datetime.strptime(rental_date_str, '%Y-%m-%d %H:%M:%S')
    get_query = """SELECT * FROM rentals"""

    with sqlite3.connect(':memory:') as connection:
        conn = connection
        execute_on_database(conn, create_table_query)
        Rental.add_rental(conn, i_user_id, i_book_id, i_rental_date)
        data = get_data_from_database(conn, get_query)

    for rental in data:
        rental_id, user_id, book_id, rental_date, return_date, returned = rental
        r_rental_id = rental_id
        r_user_id = user_id
        r_book_id = book_id
        r_rental_date = rental_date
        r_return_date = return_date
        r_returned = returned

    assert r_rental_id == 1
    assert r_user_id == user_id
    assert r_book_id == book_id
    assert r_rental_date == rental_date
    assert r_return_date == "2023-01-15 10:10:10"
    assert r_returned == 0


def test_add_rental_to_database_negative():
    create_table_query = """DROP TABLE IF EXISTS rentals;

        CREATE TABLE IF NOT EXISTS rentals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            book_id     INTEGER NOT NULL,
            rental_date TEXT    NOT NULL,
            return_date TEXT    NOT NULL,
            returned    INTEGER
    );
    """
    i_user_id = 1
    i_book_id = 1
    rental_date_str = "2023-01-01 10:10:10"
    i_rental_date =datetime.strptime(rental_date_str, '%Y-%m-%d %H:%M:%S')
    get_query = """SELECT * FROM rentals"""

    with sqlite3.connect(':memory:') as connection:
        conn = connection
        execute_on_database(conn, create_table_query)
        Rental.add_rental(conn, i_user_id, i_book_id, i_rental_date)
        data = get_data_from_database(conn, get_query)

    for rental in data:
        rental_id, user_id, book_id, rental_date, return_date, returned = rental
        r_rental_id = rental_id
        r_user_id = user_id
        r_book_id = book_id
        r_rental_date = rental_date
        r_return_date = return_date
        r_returned = returned

    assert r_rental_id != 2
    assert r_user_id != 2
    assert r_book_id != 2
    assert r_rental_date == rental_date
    assert r_return_date == "2023-01-15 10:10:10"
    assert r_returned != 1
