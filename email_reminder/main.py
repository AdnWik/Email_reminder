from sqlite3 import OperationalError
from db_conn import create_connection
from bookcase import Bookcase
from user import User
from book import Book



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
            bookcase.delete_book(conn)


    elif user_choice == '3':
        # RENTALS
        print(' RENTALS MENU '.center(50, '='))
        print('What do you want to do?')
        print("""
        1 - Show all rentals
        2 - Add rental
        3 - Update rental
        4 - Check returns
        """)
        user_choice = input(">>> ")
        if user_choice == '1':
            # SHOW ALL RENTALS
            bookcase.show_all_rentals()

        elif user_choice == '2':
            # ADD RENTAL
            bookcase.new_rental(conn)

        elif user_choice == '3':
            # UPDATE RENTAL
            pass

        elif user_choice == '4':
            # CHECK RETURNS
            bookcase.check_returns(conn)

    else:
        break
