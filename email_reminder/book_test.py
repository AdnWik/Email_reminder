import sqlite3
from book import Book
from db_conn import execute_on_database, get_data_from_database


def test_add_book_to_database_positive():
    create_table_query = """DROP TABLE IF EXISTS books;

        CREATE TABLE IF NOT EXISTS books(
	        id			INTEGER	PRIMARY KEY AUTOINCREMENT,
	        title		TEXT	NOT NULL,
	        author		TEXT	NOT NULL,
	        created_at	TEXT    NOT NULL
        );
    """
    i_title = "Generic Metal Chair"
    i_author = "Gilberto Reilly"
    i_created_at = "2022-12-03 19:06:28"
    get_query = """SELECT * FROM books"""

    with sqlite3.connect(':memory:') as connection:
        conn = connection
        execute_on_database(conn, create_table_query)
        Book.add_book(conn, i_title, i_author, i_created_at)
        data = get_data_from_database(conn, get_query)

    for book in data:
        book_id, title, author, created_at = book
        r_book_id = book_id
        r_title = title
        r_author = author
        r_created_at = created_at

    assert r_book_id == 1
    assert r_title == i_title
    assert r_author == i_author
    assert r_created_at == i_created_at


def test_add_book_to_database_negative():
    create_table_query = """DROP TABLE IF EXISTS books;

        CREATE TABLE IF NOT EXISTS books(
	        id			INTEGER	PRIMARY KEY AUTOINCREMENT,
	        title		TEXT	NOT NULL,
	        author		TEXT	NOT NULL,
	        created_at	TEXT    NOT NULL
        );
    """
    i_title = "Generic Metal Chair"
    i_author = "Gilberto Reilly"
    i_created_at = "2022-12-03 19:06:28"
    get_query = """SELECT * FROM books"""

    with sqlite3.connect(':memory:') as connection:
        conn = connection
        execute_on_database(conn, create_table_query)
        Book.add_book(conn, i_title, 'Alberta Bashirian', i_created_at)
        data = get_data_from_database(conn, get_query)

    for book in data:
        book_id, title, author, created_at = book
        r_book_id = book_id
        r_title = title
        r_author = author
        r_created_at = created_at

    assert r_book_id not in range(2, 11)
    assert r_title == i_title
    assert r_author != i_author
    assert r_created_at == i_created_at
