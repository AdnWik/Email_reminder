"""Main - Email_Reminder"""
import logging
from bookcase import (
    show_all_books,
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

# LOGGING CONFIG
logging.basicConfig(level=logging.INFO)


def show_menu_options(options: list) -> None:
    """Show menu options

    Args:
        options (list): options to show
    """
    for number, option in enumerate(options, 1):
        print(f'{number} - {option}')
    print('\nOther - EXIT')


# EMAIL REMINDER MENU
while True:
    print(' EMAIL REMINDER - MAIN MENU '.center(50, '='))
    menu_options = [
        'Users',
        'Books',
        'Rentals'
        ]

    print('Select category')
    show_menu_options(menu_options)

    user_choice = input(">>> ")
    if user_choice == '1':
        # USERS
        menu_options = [
            'Show all users',
            'Add user',
            'Delete user'
            ]

        print(' USERS MENU '.center(50, '='))
        print('What do you want to do?')
        show_menu_options(menu_options)

        user_choice = input(">>> ")
        if user_choice == '1':
            # SHOW ALL USERS
            show_all_users()

        elif user_choice == '2':
            # ADD USER
            print('Enter user first_name')
            first_name = input('>>> ')
            print('Enter user last_name')
            last_name = input('>>> ')
            print('Enter user email_address')
            email_address = input('>>> ')

            add_user(first_name, last_name, email_address)
            get_all_users()

        elif user_choice == '3':
            # DELETE USER
            delete_user()

    elif user_choice == '2':
        # BOOKS
        menu_options = [
            'Show all books',
            'Add book',
            'Delete book'
            ]

        print(' BOOKS MENU '.center(50, '='))
        print('What do you want to do?')
        show_menu_options(menu_options)

        user_choice = input(">>> ")
        if user_choice == '1':
            # SHOW ALL BOOKS
            show_all_books()

        elif user_choice == '2':
            # ADD BOOK
            print('Enter book title')
            title = input('>>> ')
            print('Enter book author')
            author = input('>>> ')
            print('Enter release date  (YYYY-MM-DD  HH:MM:SS)')
            release_date = input('>>> ')

            add_book(title, author, release_date)
            get_all_books()

        elif user_choice == '3':
            # DELETE BOOK
            delete_book()

    elif user_choice == '3':
        # RENTALS
        menu_options = [
            'Show all rentals',
            'Rent a book',
            'Return a book',
            'Check returns'
            ]

        print(' RENTALS MENU '.center(50, '='))
        print('What do you want to do?')
        show_menu_options(menu_options)

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
