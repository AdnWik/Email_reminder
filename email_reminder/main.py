from db_conn import create_connection
from bookcase import Bookcase
from rental import Rental
from sqlite3 import OperationalError
from datetime import datetime

conn = create_connection()
bookcase = Bookcase()

try:
    bookcase.get_all_books()
    bookcase.get_all_users()
except OperationalError:
    pass

bookcase.get_available_books()
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
#user_date = input('>>> ')

try:
    user_date = datetime.fromisoformat(input('>>> '))
    Rental.add_rental(conn, selected_user, selected_book, rental_date=user_date)
except ValueError:
    Rental.add_rental(conn, selected_user, selected_book)
