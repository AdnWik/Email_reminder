"""Bookcase functions
"""
from datetime import datetime, timedelta
from collections import namedtuple
import logging
from string import Template
import sqlite3
from os import getenv
from dotenv import load_dotenv
from database import Database, get_data_from_database, insert_into_database
from send_email import EmailSender

load_dotenv()
DATABASE_NAME = getenv('DB_NAME')
connection = sqlite3.connect(getenv('DB_NAME'),)


def add_user(first_name,
             last_name,
             email_address,
             db_name=DATABASE_NAME) -> None:
    """Add user to database
    """

    query = ("""insert into users (first_name, last_name, email_address)
             values(?,?,?)""")
    data = [(first_name, last_name, email_address), ]
    try:
        with Database(db_name) as database:
            database.cursor.executemany(query, data)
    except ValueError:
        pass


def add_book(title, author, release_date, db_name=DATABASE_NAME) -> None:
    """Add book to database
    Date format YYYY-MM-DD HH:MM:SS
    """

    query = ("""insert into books (title, author, created_at)
             values(?,?,?)""")
    data = [(title, author, release_date), ]
    try:
        with Database(db_name) as database:
            database.cursor.executemany(query, data)
    except ValueError:
        pass


def get_all_books(db_name=DATABASE_NAME) -> list:
    """Get all books from database

    Returns:
        list: books from database
    """

    field_names = ['book_id',
                   'title',
                   'author',
                   'created_at']
    book_tuple = namedtuple('Book', field_names)
    books = []
    query = "SELECT * FROM books"

    try:
        with Database(db_name) as database:
            database.cursor.execute(query)
            data = database.cursor.fetchall()
        if data:
            for book in map(book_tuple._make, data):
                books.append(book)
            return books
        else:
            return None
    except ValueError:
        return None


def get_all_users(db_name=DATABASE_NAME) -> list:
    """Get all users from database

    Returns:
        list: users from database
    """

    field_names = ['user_id',
                   'first_name',
                   'last_name',
                   'email_address']
    user_tuple = namedtuple('User', field_names)
    users = []
    query = "SELECT * FROM users"

    try:
        with Database(db_name) as database:
            database.cursor.execute(query)
            data = database.cursor.fetchall()
        if data:
            for user in map(user_tuple._make, data):
                users.append(user)
            return users
        else:
            return None
    except ValueError:
        return None


def get_all_rentals(db_name=DATABASE_NAME) -> list:
    """Get all rentals from database

    Returns:
        list: rentals from database
    """

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
        with Database(db_name) as database:
            database.cursor.execute(query)
            data = database.cursor.fetchall()
        if data:
            for rental in map(rental_tuple._make, data):
                rentals.append(rental)
            return rentals
        else:
            return None
    except ValueError:
        return None


def add_rental(user_id,
               book_id,
               rental_date=datetime.now(),
               days_of_rental=14,
               returned=False,
               db_name=DATABASE_NAME) -> None:
    """Add rental record to database
    """

    ret_date = (rental_date +
                timedelta(days=days_of_rental)).strftime('%Y-%m-%d %H:%M:%S')
    rental_date_formatted = rental_date.strftime('%Y-%m-%d %H:%M:%S')

    ret = None
    if not returned:
        ret = 0
    else:
        ret = 1
    data = [(user_id, book_id, rental_date_formatted, ret_date, ret), ]
    query = """insert into rentals (user_id,
                                    book_id,
                                    rental_date,
                                    return_date,
                                    returned)
                values (?, ?, ?, ?, ?)"""

    insert_into_database(query, data)


def new_rental(db_name=DATABASE_NAME) -> None:
    """Add new rental to database
    """

    available_books = get_available_books()
    users = get_all_users()
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
    print('Enter rent date (YYYY-MM-DD  HH:MM:SS):' +
          '   (If today press enter)')

    try:
        user_date = datetime.fromisoformat(input('>>> '))
        add_rental(selected_user, selected_book, rental_date=user_date)
    except ValueError:
        add_rental(selected_user, selected_book)

    print('Rental successful added')


def check_returns(db_name=DATABASE_NAME) -> None:
    """Check returns in database for date 'now'
    """

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
                        STRFTIME('%J',JULIANDAY('now') -
                        JULIANDAY(t1.return_date)) AS delayed_days
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
                  f' Delayed: {float(rental.delayed_days):.0f} days')

        print(f'\nYou have {len(delayed_rentals)} delayed rentals')
        print('Do you want send email reminders? (y/N)')

        user_choice = input(">>> ")
        if user_choice == 'y':
            send_email_reminder(delayed_rentals)


def get_available_books(db_name=DATABASE_NAME) -> list:
    """Get all not rented books from database

    Returns:
        list: not rented books from database
    """

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


def show_all_users(db_name=DATABASE_NAME) -> None:
    """Show all users from database
    """

    users = get_all_users()
    for no, user in enumerate(users, 1):
        print(f'{no} - {user.first_name}'
              f' {user.last_name} ({user.email_address})')


def show_all_books(db_name=DATABASE_NAME) -> None:
    """Show all books from database
    """

    books = get_all_books()
    for no, book in enumerate(books, 1):
        print(f'{no} - {book.title} {book.author}')


def show_all_rentals(db_name=DATABASE_NAME) -> None:
    """Show all rentals from database
    """

    rentals = get_all_rentals()
    for no, rental in enumerate(rentals, 1):
        print(f'{no:<3} - {rental.email_address:<20}'
              f' {rental.title:<30} {rental.author:<30}'
              f' {rental.rental_date:<20} {rental.return_date:<20}'
              f' {rental.returned:<2}')


def delete_book(db_name=DATABASE_NAME) -> None:
    """Remove book from database
    """

    available_books = get_available_books()
    if len(available_books) == 0:
        print('NO BOOKS AVAILABLE TO DELETE'.center(50, '='))
    else:
        print('BOOKS AVAILABLE TO DELETE'.center(50, '='))
        for book_no, book in enumerate(available_books, 1):
            print(f'{book_no} -> {book} ')

        print('\nChose book to delete')
        user_choice = int(input('>>> '))
        book_to_delete = available_books[user_choice - 1]

        query = """DELETE FROM books WHERE id = ?"""
        data = [(str(book_to_delete.book_id), ), ]

        print(f'\nDo you want delete "{book_to_delete.title} -'
              f' {book_to_delete.author}"?')
        print('Y/n ?')
        user_choice = input('>>> ')
        if user_choice == 'Y':
            try:
                insert_into_database(query, data)
                print(f'Book "{book_to_delete.title} -'
                      f' {book_to_delete.author}" has been deleted')
            except ValueError:
                pass


def delete_user(db_name=DATABASE_NAME) -> None:
    """Remove user from database if user returned all borrow books
    """

    # Select users with rentals
    query = """SELECT   t2.user_id,
    t2.first_name,
    t2.last_name,
    t2.email_address,
    COUNT(t1.user_id) AS rented_books,
    CASE
        WHEN t1.returned = 1 THEN COUNT(t1.returned)
        ELSE 0 END AS returned_books
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
                print(f'User "{selected_user.first_name}'
                      f' {selected_user.last_name}" has been deleted')
            except ValueError as error:
                print(str(error))


def return_book(db_name=DATABASE_NAME) -> None:
    """Return borrowed book
    """

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
        print(f'{no} -> Book: {rental.book_title:<30}'
              f' {rental.book_author:<30} | User: {rental.user_first_name:<20}'
              f' {rental.user_last_name:<20} {rental.user_email}')

    print('\nWitch book do you want to return?')
    userChoice = int(input(">>> "))
    if userChoice != 0:
        try:
            rental_idx = userChoice - 1
            query = ("""UPDATE rentals SET returned = 1
                     WHERE rental_id = ?""")
            data = [(str(rentals[rental_idx].rental_id)), ]
            insert_into_database(query, data)
            print('Book: successful returned')
        except ValueError:
            pass


def send_email_reminder(data, db_name=DATABASE_NAME) -> None:
    """Send email reminder for users with delayed rentals
    """
    server = getenv('SERVER')
    port = getenv('PORT')
    username = getenv('MAIL_USERNAME')
    password = getenv('MAIL_PASSWORD')
    Credentials = namedtuple('User', 'username, password')
    credentials = Credentials(username, password)

    message_template = Template(
        """$name get back my book! ($title - $author)
You were supposed to give it back to me $days days ago.

I'm waiting!""")

    with EmailSender(port, server, credentials) as connection:
        for record in data:
            sender = getenv('SENDER')
            receiver = (f"{record.user_first_name} {record.user_last_name}"
                        f" <{record.user_email}>")
            subject = (f'Subject: Book "{record.book_title}"'
                       f' return delayed!\n')

            message = message_template.substitute({
                'name': record.user_first_name,
                'title': record.book_title,
                'author': record.book_author,
                'days': format(float(record.delayed_days), '.0f')
            })

            connection.send_email(sender, receiver, subject, message)
            logging.info(f'Email sended to {record.user_email}')
