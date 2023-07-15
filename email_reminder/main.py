"""Main - Email_Reminder"""
import logging
from bookcase import Bookcase

# LOGGING
logging.basicConfig(level=logging.INFO)

# EMAIL REMINDER MENU
bookcase = Bookcase()
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
            bookcase.show_all_users()

        elif user_choice == '2':
            # ADD USER
            bookcase.add_user()
            bookcase.get_all_users()

        elif user_choice == '3':
            # DELETE USER
            bookcase.delete_user()

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
            bookcase.add_book()
            bookcase.get_all_books()

        elif user_choice == '3':
            # DELETE BOOK
            bookcase.delete_book()

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
            bookcase.show_all_rentals()

        elif user_choice == '2':
            # RENT A BOOK
            bookcase.new_rental()

        elif user_choice == '3':
            # RETURN A BOOK
            bookcase.return_book()

        elif user_choice == '4':
            # CHECK RETURNS
            bookcase.check_returns()

    else:
        break
