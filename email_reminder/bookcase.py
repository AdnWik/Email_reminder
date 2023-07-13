from datetime import datetime
from collections import namedtuple
import logging
import smtplib
from database import get_data_from_database, insert_into_database
from rental import Rental



class Bookcase:

    @staticmethod
    def add_user():
        print('Enter user first_name')
        first_name = input('>>> ')
        print('Enter user last_name')
        last_name = input('>>> ')
        print('Enter user email_address')
        email_address = input('>>> ')

        query = """insert into users (first_name, last_name, email_address) values(?,?,?)"""
        data = [(first_name, last_name, email_address), ]
        try:
            insert_into_database(query, data)
        except ValueError:
            pass

    @staticmethod
    def add_book():
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
            insert_into_database(query, data)
        except ValueError:
            pass

    @staticmethod
    def get_all_books() -> list:
        field_names = ['book_id',
                       'title',
                       'author',
                       'created_at']
        book_tuple = namedtuple('Book', field_names)
        books = []
        query = "SELECT * FROM books"

        try:
            data = get_data_from_database(query)
            if data:
                for book in map(book_tuple._make, data):
                    books.append(book)
                return books
            else:
                return None
        except ValueError:
            return None

    @staticmethod
    def get_all_users() -> list:
        field_names = ['user_id',
                       'first_name',
                       'last_name',
                       'email_address']
        user_tuple = namedtuple('User', field_names)
        users = []
        query = "SELECT * FROM users"

        try:
            data = get_data_from_database(query)
            if data:
                for user in map(user_tuple._make, data):
                    users.append(user)
                return users
            else:
                return None
        except ValueError:
            return None

    @staticmethod
    def get_all_rentals() -> list:
        field_names = ['email_address',
                       'title',
                       'author',
                       'rental_date',
                       'return_date',
                       'returned']
        rental_tuple = namedtuple('Rental', field_names)
        rentals = []
        query = """SELECT   t2.email_address,
                            t3.title,
                            t3.author,
                            t1.rental_date,
                            t1.return_date,
                            t1.returned
                    FROM rentals AS t1
                    LEFT JOIN users AS t2
                    ON t1.user_id = t2.user_id
                    LEFT JOIN books AS t3
                    ON t1.book_id = t3.id"""

        try:
            data = get_data_from_database(query)
            if data:
                for rental in map(rental_tuple._make, data):
                    rentals.append(rental)
                return rentals
            else:
                return None
        except ValueError:
            return None

    @staticmethod
    def new_rental():
        available_books = Bookcase.get_available_books()
        users = Bookcase.get_all_users()
        print('New rental'.center(50, '-'))
        print('Chose user')
        for No, user in enumerate(users, 1):
            print(f'{No} - {user.first_name} {user.last_name}')

        user_index = int(input('>>> '))
        selected_user = users[user_index - 1].user_id

        print('\n')
        print('Chose book to rent')
        for No, book in enumerate(available_books, 1):
            print(f'{No} - {book.title}')
        book_index = int(input('>>> '))
        selected_book = available_books[book_index - 1].book_id

        print('\n')
        print(f'Enter rent date (YYYY-MM-DD  HH:MM:SS):'
              f'   (If today press enter)')

        try:
            user_date = datetime.fromisoformat(input('>>> '))
            Rental.add_rental(conn, selected_user, selected_book, rental_date=user_date)
        except ValueError:
            Rental.add_rental(conn, selected_user, selected_book)

        print('Rental successful added')

    @staticmethod
    def check_returns():
        field_names = ['book_title',
                       'book_author',
                       'user_first_name',
                       'user_last_name',
                       'user_email',
                       'return_date',
                       'delayed_days']
        rental_tuple = namedtuple('Rental', field_names)
        delayed_rentals = []
        query = """SELECT   t3.title,
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

        data = get_data_from_database(query)
        if not data:
            print('You have not delayed rentals')
        else:
            for rental in map(rental_tuple._make, data):
                delayed_rentals.append(rental)

            for rental in delayed_rentals:
                print(f'User email: {rental.user_email:<40}'
                      f' Return date: {rental.return_date:<20}'
                      f' Delayed: {float(rental.delayed_days):.1f} days')

            print(f'\nYou have {len(delayed_rentals)} delayed rentals')
            print('Do you want send email reminders? (y/N)')

            user_choice = input(">>> ")
            if user_choice == 'y':
                Bookcase.send_email_reminder(delayed_rentals)


    @staticmethod
    def get_available_books() -> list:
        field_names = ['book_id',
                       'title',
                       'author',
                       'created_at']
        book_tuple = namedtuple('Book', field_names)
        available_books = []
        query = """SELECT * FROM books
                    EXCEPT
                    SELECT	t1.*
                    FROM books AS t1
                    LEFT JOIN rentals AS t2
                    ON t1.id = t2.book_id
                    WHERE t2.returned = 0"""
        try:
            data = get_data_from_database(query)
            if data:
                for book in map(book_tuple._make, data):
                    available_books.append(book)
                return available_books
            else:
                return None
        except ValueError:
            return None

    @staticmethod
    def show_all_users():
        users = Bookcase.get_all_users()
        for no, user in enumerate(users, 1):
            print(f'{no} - {user.first_name}'
                  f' {user.last_name} ({user.email_address})')

    @staticmethod
    def show_all_books():
        books = Bookcase.get_all_books()
        for no, book in enumerate(books, 1):
            print(f'{no} - {book.title} {book.author}')

    @staticmethod
    def show_all_rentals():
        rentals = Bookcase.get_all_rentals()
        for no, rental in enumerate(rentals, 1):
            print(f'{no} - {rental.email_address:<20}'
                  f' {rental.title:<30} {rental.author:<30}'
                  f' {rental.rental_date:<20} {rental.return_date:<20}'
                  f' {rental.returned:<2}')

    @staticmethod
    def delete_book():
        available_books = Bookcase.get_available_books()
        if len(available_books) == 0:
            print('NO BOOKS AVAILABLE TO DELETE'.center(50, '='))
        else:
            print('BOOKS AVAILABLE TO DELETE'.center(50, '='))
            for book_no, book in enumerate(available_books, 1):
                print(f'{book_no} -> {book} ')

            print('\nChose book to delete')
            user_choice = int(input('>>> '))
            for book_no, book in enumerate(available_books, 1):
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
                    insert_into_database(query, data)
                    print(f'Book "{book_to_delete}" has been deleted')
                except ValueError:
                    pass

    @staticmethod
    def delete_user():
        # Select users with rentals
        query = """SELECT   t2.user_id,
        t2.first_name,
        t2.last_name,
        t2.email_address,
        COUNT(t1.user_id) AS rented_books,
        CASE
            WHEN t1.returned = 1 THEN COUNT(t1.returned) ELSE 0 END AS returned_books
        FROM rentals AS t1
        LEFT JOIN users AS t2
        ON t1.user_id = t2.user_id
        GROUP BY t1.user_id"""

        # Select users without any rentals
        query_2 = """SELECT user_id,
        first_name,
        last_name,
        email_address
        FROM users
        EXCEPT
        SELECT	t2.user_id,
        t2.first_name ,
        t2.last_name ,
        t2.email_address
        FROM rentals AS t1
        LEFT JOIN users AS t2
        ON t1.user_id = t2.user_id"""

        data = []
        users_available_to_del = []
        users_with_rentals = get_data_from_database(query)
        users_without_rentals = get_data_from_database(query_2)

        if users_with_rentals:
            data.extend(users_with_rentals)

        if users_without_rentals:
            users_without_rentals[0] += (0, 0, )
            data.extend(users_without_rentals)

        if not data:
            logging.info('NO DATA FROM DATABASE')
        else:
            fields_name = ['user_id',
                           'first_name',
                           'last_name',
                           'email_address',
                           'rented_books',
                           'returned_books']
            user_namedtuple = namedtuple('user', fields_name, defaults=[0, 0])
            for user in map(user_namedtuple._make, data):
                if user.rented_books == user.returned_books:
                    users_available_to_del.append(user)
            logging.info('USERS CREATED')

        if not users_available_to_del:
            print('NO USERS AVAILABLE TO DELETE'.center(50, '='))
        else:
            print('USERS AVAILABLE TO DELETE'.center(50, '='))
            for user_no, user in enumerate(users_available_to_del, 1):
                print(f'{user_no} -> {user.first_name} {user.last_name}'
                      f' {user.email_address} {user.email_address}')
            print('\nWhich user do you want to delete ?')
            user_choice = int(input('>>> '))
            selected_user = users_available_to_del[user_choice - 1]
            print(f'Selected user: {selected_user.first_name}'
                  f' {selected_user.last_name} {selected_user.email_address}')
            print('Do you want remove it? (Y/n)')
            user_choice = input('>>> ')
            if user_choice == 'Y':
                query = """DELETE FROM users
                    WHERE user_id = ?"""
                data = [(str(selected_user.user_id)), ]
                try:
                    insert_into_database(query, data)
                    print(f'User "{selected_user.first_name} {selected_user.last_name}" has been deleted')
                except ValueError as error:
                    print(str(error))

    @staticmethod
    def return_book():
        field_names = ['rental_id',
                       'book_title',
                       'book_author',
                       'user_first_name',
                       'user_last_name',
                       'user_email',
                       'return_date']
        rental_tuple = namedtuple('Rental', field_names)
        rentals = []
        query = """SELECT   t1.rental_id,
                            t3.title,
                            t3.author,
                            t2.first_name,
                            t2.last_name,
                            t2.email_address,
                            t1.return_date
                    FROM rentals AS t1
                    LEFT JOIN users AS t2
                    ON t1.user_id = t2.user_id
                    LEFT JOIN books AS t3
                    ON t1.book_id = t3.id
                    WHERE t1.returned = 0"""

        data = get_data_from_database(query)
        if data:
            for rental in map(rental_tuple._make, data):
                rentals.append(rental)

        print(' RENTALS AVAILABLE TO RETURN'.center(50, '='))
        for no, rental in enumerate(rentals, 1):
            print(f'{no} -> Book: {rental.book_title:<30} {rental.book_author:<30} | User: {rental.user_first_name:<20} {rental.user_last_name:<20} {rental.user_email}')

        print('\nWitch book do you want to return?')
        userChoice = int(input(">>> "))
        if userChoice != 0:
            try:
                rental_idx = userChoice - 1
                query = """UPDATE rentals SET returned = 1 WHERE rental_id = ?"""
                data = [(str(rentals[rental_idx].rental_id)), ]
                insert_into_database(query, data)
                print('Book: successful returned')
            except ValueError:
                pass

    def send_email_reminder(data):
        """Send email reminder for delayed rentals"""
        sender = "Private Person <from@example.com>"
        receiver = "A Test User <to@example.com>"

        message = (f"Subject: Hi Mailtrap\n"
                   f"To: {receiver}\nFrom: {sender}\n\n"
                   f"This is a test e-mail message.")

        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.login("c3a9f81f95780c", "0512af4507550d")
            server.sendmail(sender, receiver, message)
            logging.info('Email send')
