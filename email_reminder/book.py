from sqlite3 import OperationalError
from db_conn import insert_into_database


class Book:

    def __init__(self, book_id, title, author, created_at) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.created_at = created_at

    def __repr__(self) -> str:
        return f'{self.title} - {self.author}'

    def __str__(self) -> str:
        return f'{self.title} - {self.author}'

    @staticmethod
    def add_book(conn):
        # Date fromat YYYY-MM-DD HH:MM:SS
        print('Enter book title')
        title = input('>>> ')
        print('Enter book author')
        author = input('>>> ')
        print('Enter book title')
        release_date = input('>>> ')

        query = """insert into books (title, author, created_at) values(?,?,?)"""
        data = [(title, author, release_date), ]
        try:
            insert_into_database(conn, query, data)
        except OperationalError:
            pass
