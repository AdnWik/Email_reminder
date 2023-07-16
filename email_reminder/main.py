"""Main - Email_Reminder"""
import logging
from bookcase import (show_all_books,
                      show_all_rentals,
                      show_all_users,
                      add_book,
                      add_user,
                      get_all_books,
                      get_all_users,
                      delete_book,
                      delete_user,
                      new_rental,
                      return_book,
                      check_returns
                      )

# LOGGING
logging.basicConfig(level=logging.INFO)

# EMAIL REMINDER MENU
print(' EMAIL REMINDER '.center(50, '='))
while True:
    print('-'*50)
    print('Select category')
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
            show_all_users()

        elif user_choice == '2':
            # ADD USER
            add_user()
            get_all_users()

        elif user_choice == '3':
            # DELETE USER
            delete_user()

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
            show_all_books()

        elif user_choice == '2':
            # ADD BOOK
            add_book()
            get_all_books()

        elif user_choice == '3':
            # DELETE BOOK
            delete_book()

    elif user_choice == '3':
        # RENTALS
        print(' RENTALS MENU '.center(50, '='))
        print('What do you want to do?')
        print("""
1 - Show all rentals
2 - Rent a book
3 - Return a book
4 - Check returns
""")
        user_choice = input(">>> ")
        if user_choice == '1':
            # SHOW ALL RENTALS
            show_all_rentals()

        elif user_choice == '2':
            # RENT A BOOK
            new_rental()

        elif user_choice == '3':
            # RETURN A BOOK
            return_book()

        elif user_choice == '4':
            # CHECK RETURNS
            check_returns()

    else:
        break
