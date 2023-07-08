from sqlite3 import OperationalError
from datetime import datetime
from db_conn import get_data_from_database,insert_into_database
from book import Book
from user import User
from rental import Rental



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

    def new_rental(self, conn):
        self.get_available_books(conn)
        print('New rental'.center(50, '-'))
        print('Chose user')
        for No, user in enumerate(self.users, 1):
            print(f'{No} - {user.name}')

        user_index = int(input('>>> '))
        selected_user = self.users[user_index - 1].user_id

        print('\n')
        print('Chose book to rent')
        for No, book in enumerate(self.books, 1):
            print(f'{No} - {book.title}')
        book_index = int(input('>>> '))
        selected_book = self.books[book_index - 1].book_id

        print('\n')
        print('Enter rent date (YYYY-MM-DD  HH:MM:SS):   (If today press enter)')

        try:
            user_date = datetime.fromisoformat(input('>>> '))
            Rental.add_rental(conn, selected_user, selected_book, rental_date=user_date)
        except ValueError:
            Rental.add_rental(conn, selected_user, selected_book)


    def check_returns(self, conn):
        query = """SELECT	t3.title,
                            t3.author,
                            t2.first_name,
                            t2.last_name,
                            t2.email_address,
                            t1.return_date,
                            STRFTIME('%J',JULIANDAY('now') - JULIANDAY(t1.return_date)) AS delayed_days
                    FROM rentals AS t1
                    LEFT JOIN users AS t2
                    ON t1.user_id = t2.user_id
                    LEFT JOIN books AS t3
                    ON t1.book_id = t3.id
                    WHERE datetime(t1.return_date) < datetime('now')
                    AND t1.returned = 0"""
        data = get_data_from_database(conn, query)
        for record in data:
            book_title, book_author, user_first_name, user_last_name, user_email, return_date, delayed_days = record
            delayed_days_formatted = float(delayed_days)
            print(f'User email: {user_email:<40} Return date: {return_date:<20} Delayed: {delayed_days_formatted:.1f} days')

        delayed_rentals_number = len(data)
        if delayed_rentals_number == 0:
            print('You have not delayed rentals')

        elif delayed_rentals_number > 0:
            print(f'\nYou have {delayed_rentals_number} delayed rentals')
            print('Do you want send email reminders? (y/N)')
            input(">>> ")

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

    def delete_book(self, conn):
        self.get_available_books(conn)
        print('BOOKS AVAILABLE TO DELETE'.center(50, '='))
        for book_no, book in enumerate(self.books, 1):
            print(f'{book_no} -> {book} ')

        print('\nChose book to delete')
        user_choice = int(input('>>> '))
        for book_no, book in enumerate(self.books, 1):
            if user_choice == book_no:
                book_to_delete = book

        query = """DELETE FROM books
                   WHERE id = ?"""
        data = [(str(book_to_delete.book_id)), ]

        print(f'\nDo you want delete "{book_to_delete}"?')
        print('Y/n ?')
        user_choice = input('>>> ')
        if user_choice == 'Y':
            try:
                insert_into_database(conn, query, data)
                print(f'Book "{book_to_delete}" has been deleted')
            except OperationalError:
                pass

    def delete_user(self, conn):
        pass
