from db_conn import insert_into_database
from datetime import datetime


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
    def add_book(conn, title, author, created_at):
        # Date fromat YYYY-MM-DD HH:MM:SS
        created = created_at
        query = """insert into books (title, author, created_at) values(?,?,?)"""
        data = [(title, author, created), ]
        insert_into_database(conn, query, data)
