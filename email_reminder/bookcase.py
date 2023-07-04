from db_conn import create_connection, get_data_from_database
from book import Book
from user import User


class Bookcase:

    def __init__(self) -> None:
        self.books = []
        self.users = []

    def get_all_books(self) -> None:
        query = "select * from books"
        conn = create_connection()
        data = get_data_from_database(conn, query)

        print(f'Books: {data}')
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

        print(f'Books: {data}')
        for user in data:
            user_id, first_name, last_name, email_address = user
            self.users.append(User(
                user_id,
                first_name,
                last_name,
                email_address
            ))
