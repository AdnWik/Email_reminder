from db_conn import get_data_from_database
from book import Book
from user import User
from rental import Rental
from sqlite3 import OperationalError


class Bookcase:

    def __init__(self) -> None:
        self.books = []
        self.users = []
        self.rentals = []

    def get_all_books(self, conn) -> None:
        query = "select * from books"

        try:
            data = get_data_from_database(conn, query)
            self.books = []
            for book in data:
                book_id, title, author, created_at = book
                self.books.append(Book(
                    book_id,
                    title,
                    author,
                    created_at
                ))
        except OperationalError:
            pass

    def get_all_users(self, conn) -> None:
        query = "select * from users"
        try:
            data = get_data_from_database(conn, query)
            self.users = []
            for user in data:
                user_id, first_name, last_name, email_address = user
                self.users.append(User(
                    user_id,
                    first_name,
                    last_name,
                    email_address
                ))
        except OperationalError:
            pass

    def get_all_rentals(self, conn) -> None:
        query = "select * from rentals"
        try:
            data = get_data_from_database(conn, query)
            self.rentals = []
            for rental in data:
                rental_id, user_id, book_id, rental_date, return_date, returned = rental
                self.rentals.append(Rental(
                    rental_id,
                    user_id,
                    book_id,
                    rental_date,
                    return_date,
                    returned
                ))
        except OperationalError:
            pass

    def get_available_books(self, conn):
        self.books = []
        query = """SELECT * FROM books
                    EXCEPT
                    SELECT	t1.*
                    FROM books AS t1
                    LEFT JOIN rentals AS t2
                    ON t1.id = t2.book_id
                    WHERE t2.returned = 0"""
        data = get_data_from_database(conn, query)

        for book in data:
            book_id, title, author, created_at = book
            self.books.append(Book(
                book_id,
                title,
                author,
                created_at
            ))

    def show_all_users(self):
        for user in self.users:
            print(user)

    def show_all_books(self):
        for book in self.books:
            print(book)

    def show_all_rentals(self):
        for rental in self.rentals:
            print(rental)