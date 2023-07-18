import sqlite3
import pytest
from bookcase import get_all_books

@pytest.fixture
def create_connection():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE books(
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                author      TEXT    NOT NULL,
                created_at  DATE    NOT NULL)""")

    cur.execute("""CREATE TABLE users (
                user_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name      TEXT    NOT NULL,
                last_name       TEXT    NOT NULL,
                email_address   TEXT    NOT NULL)""")

    cur.execute("""CREATE TABLE rentals (
                rental_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                book_id     INTEGER NOT NULL,
                rental_date TEXT    NOT NULL,
                return_date TEXT    NOT NULL,
                returned    INTEGER NOT NULL)""")

    sample_books_data = [
        ('W Pustyni i w Puszczy', 'Henryk Sienkiewicz', '2020-02-03 12:30:50'),
        ('Dzieci z Bullerbyn', 'Astrid Lindgren', '2019-01-02 11:31:31'),
        ('Mały Książe', 'Antonie de Saint-Exupery', '2010-01-01 11:10:10'),
        ('Mistrz i Małgorzata', 'Michaił Bułhakow', '2021-04-23 22:30:10')
    ]

    sample_users_data = [
        ('Anastacio', 'Aufderhar', 'a.aufderhar@example.com'),
        ('Ona', 'Toy', 'o.toy@example.com'),
        ('Reta', 'Lockman', 'r.lockman@example.com'),
    ]

    sample_rentals_data = [
        ('1', '1', '2023-07-04 19:30:30', '2023-07-18 19:30:30', 1),
        ('2', '2', '2023-07-04 19:30:30', '2023-07-18 19:30:30', 0),
        ('3', '3', '2023-07-04 19:30:30', '2023-07-18 19:30:30', 1)

    ]

    cur.executemany("""INSERT INTO books(
                    title,
                    author,
                    created_at
                    )
                VALUES(?,?,?)""", sample_books_data)

    cur.executemany("""INSERT INTO users (
                    first_name,
                    last_name,
                    email_address
                    )
                VALUES (?,?,?)""", sample_users_data)

    cur.executemany("""INSERT INTO rentals (
                    user_id,
                    book_id,
                    rental_date,
                    return_date, returned
                    )
                VALUES (?,?,?,?,?)""", sample_rentals_data)

    return conn


def test_get_all_books(create_connection):
    books = get_all_books(create_connection)
    assert len(books) == 4
    assert books[3][2] == 'Michaił Bułhakow'
