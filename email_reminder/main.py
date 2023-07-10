from db_conn import create_connection
from bookcase import Bookcase


conn = create_connection()
bookcase = Bookcase()

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
            bookcase.show_all_users(conn)
            pass

        elif user_choice == '2':
            # ADD USER
            bookcase.add_user(conn)
            bookcase.get_all_users(conn)

        elif user_choice == '3':
            # DELETE USER
            bookcase.delete_user(conn)

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
            bookcase.show_all_books(conn)

        elif user_choice == '2':
            # ADD BOOK
            bookcase.add_book(conn)
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
            bookcase.show_all_rentals(conn)

        elif user_choice == '2':
            # ADD RENTAL
            bookcase.new_rental(conn)

        elif user_choice == '3':
            # UPDATE RENTAL
            # TODO:
            pass

        elif user_choice == '4':
            # CHECK RETURNS
            bookcase.check_returns(conn)

    else:
        break
