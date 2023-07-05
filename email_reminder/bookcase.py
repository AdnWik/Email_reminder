from db_conn import create_connection, get_data_from_database
from book import Book
from user import User
from rental import Rental


class Bookcase:

    def __init__(self) -> None:
        self.books = []
        self.users = []
        self.rentals = []

    def get_all_books(self) -> None:
        query = "select * from books"
        conn = create_connection()
        data = get_data_from_database(conn, query)

        for book in data:
            book_id, title, author, created_at = book
            self.books.append(Book(
                book_id,
                title,
                author,
                created_at
            ))

    def get_all_users(self) -> None:
        query = "select * from users"
        conn = create_connection()
        data = get_data_from_database(conn, query)

        for user in data:
            user_id, first_name, last_name, email_address = user
            self.users.append(User(
                user_id,
                first_name,
                last_name,
                email_address
            ))

    def get_all_rentals(self) -> None:
        query = "select * from rentals"
        conn = create_connection()
        data = get_data_from_database(conn, query)

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

    def get_available_books(self):
        self.books = []
        query = """SELECT * FROM books
                    EXCEPT
                    SELECT	t1.*
                    FROM books AS t1
                    LEFT JOIN rentals AS t2
                    ON t1.id = t2.book_id
                    WHERE t2.returned = 0"""
        conn = create_connection()
        data = get_data_from_database(conn, query)

        for book in data:
            book_id, title, author, created_at = book
            self.books.append(Book(
                book_id,
                title,
                author,
                created_at
            ))