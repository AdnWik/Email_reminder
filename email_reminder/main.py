import sqlite3


def create_connection():
    with sqlite3.connect('base.db') as connection:
        cursor = connection.cursor()
    return cursor

def get_all_books(cursor):
    cursor.execute('select * from books')
    data = []

    for book in cursor.fetchall():
        book_id, title, author, created_at = book
        data.append({
             'title': title,
             'author': author
            })

    return data


cursor = create_connection()
books = get_all_books(cursor)
print(books)
