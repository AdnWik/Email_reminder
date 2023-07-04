from db_conn import create_connection
from bookcase import Bookcase
from rental import Rental
from book import Book
from user import User
from sqlite3 import OperationalError

conn = create_connection()
bookcase = Bookcase()

try:
    bookcase.get_all_books()
    bookcase.get_all_users()
except OperationalError:
    pass


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

Rental.add_rental(conn, selected_user, selected_book)
