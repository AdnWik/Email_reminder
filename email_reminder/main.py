from bookcase import Bookcase
import sqlite3


bookcase = Bookcase()
try:
    bookcase.get_all_books()
except sqlite3.OperationalError:
    pass

try:
    bookcase.get_all_users()
except sqlite3.OperationalError:
    pass
print(bookcase.books)
print(bookcase.users)
