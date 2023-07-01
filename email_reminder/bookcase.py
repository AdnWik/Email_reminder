from db_conn import create_connection
from book import Book
from user import User


class Bookcase:

    def __init__(self) -> None:
        self.books = []
        self.users = []

    def get_all_books(self) -> None:
        cur = create_connection()
        cur.execute("select * from books")

        for book in cur.fetchall():
            book_id, title, author, created_at = book
            self.books.append(Book(
                book_id,
                title,
                author,
                created_at
            ))

    def get_all_users(self) -> None:
        cur = create_connection()
        cur.execute("select * from users")

        for user in cur.fetchall():
            user_id, first_name, last_name, email_address = user
            self.users.append(User(
                user_id,
                first_name,
                last_name,
                email_address
            ))
