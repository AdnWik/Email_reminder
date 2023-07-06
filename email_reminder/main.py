from db_conn import create_connection
from bookcase import Bookcase
from rental import Rental
from user import User
from book import Book
from sqlite3 import OperationalError
from datetime import datetime


def new_rental(conn):
    bookcase.get_available_books(conn)
    print('New rental'.center(50, '-'))
    print('Chose user')
    for No, user in enumerate(bookcase.users, 1):
        print(f'{No} - {user.name}')

    user_index = int(input('>>> '))
    selected_user = bookcase.users[user_index - 1].user_id

    print('\n')
    print('Chose book to rent')
    for No, book in enumerate(bookcase.books, 1):
        print(f'{No} - {book.title}')
    book_index = int(input('>>> '))
    selected_book = bookcase.books[book_index - 1].book_id

    print('\n')
    print('Enter rent date (YYYY-MM-DD  HH:MM:SS):   (If today press enter)')

    try:
        user_date = datetime.fromisoformat(input('>>> '))
        Rental.add_rental(conn, selected_user, selected_book, rental_date=user_date)
    except ValueError:
        Rental.add_rental(conn, selected_user, selected_book)


conn = create_connection()
bookcase = Bookcase()

try:
    bookcase.get_all_books(conn)
    bookcase.get_all_users(conn)
    bookcase.get_all_rentals(conn)
except OperationalError:
    pass

print(' EMAIL REMINDER '.center(50, '='))
while True:
    print('-'*50)
    print('What do you want to do?')
    print("""
    1 - Users
    2 - Books
    3 - Rentals

    Other - Exit""")
    user_choice = input(">>> ")
    if user_choice == '1':
        # USERS
        print(' USERS MENU '.center(50, '='))
        print('What do you want to do?')
        print("""
        1 - Show all users
        2 - Add user
        3 - delete user
        """)
        user_choice = input(">>> ")
        if user_choice == '1':
            # SHOW ALL USERS
            bookcase.show_all_users()
            pass

        elif user_choice == '2':
            # ADD USER
            User.add_user(conn)
            bookcase.get_all_users(conn)

        elif user_choice == '3':
            # DELETE USER
            pass

    elif user_choice == '2':
        # BOOKS
        print(' BOOKS MENU '.center(50, '='))
        print('What do you want to do?')
        print("""
        1 - Show all books
        2 - Add book
        3 - delete book
        """)
        user_choice = input(">>> ")
        if user_choice == '1':
            # SHOW ALL BOOKS
            bookcase.show_all_books()

        elif user_choice == '2':
            # ADD BOOK
            Book.add_book(conn)
            bookcase.get_all_books(conn)

        elif user_choice == '3':
            # DELETE BOOK
            pass


    elif user_choice == '3':
        # RENTALS
        print(' RENTALS MENU '.center(50, '='))
        print('What do you want to do?')
        print("""
        1 - Show all rentals
        2 - Add rental
        3 - Check returns
        """)
        user_choice = input(">>> ")
        if user_choice == '1':
            # SHOW ALL RENTALS
            bookcase.show_all_rentals()

        elif user_choice == '2':
            # ADD RENTAL
            new_rental(conn)

        elif user_choice == '3':
            # CHECK RETURNS
            pass

    else:
        break
