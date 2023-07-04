from db_conn import insert_into_database
from datetime import datetime, timedelta
import logging

class Rental:

    def __init__(self, rental_id, user_id, book_id, rental_date, return_date, returned) -> None:
        self.rental_id = rental_id
        self.user_id = user_id
        self.book_id = book_id
        self.rental_date = rental_date
        self.return_date = return_date
        if returned == 0:
            self.returned = False
        else:
            self.returned = True

    def __repr__(self) -> str:
        return f'{self.user_id} -> {self.book_id}'

    def __str__(self) -> str:
        return f'{self.user_id} -> {self.book_id} Return date: {self.return_date} Returned: {self.returned}'


    @staticmethod
    def add_rental(conn, user_id, book_id, rental_date=datetime.now(), days_of_rental=14, returned=False):

        return_date = (rental_date + timedelta(days=days_of_rental)).strftime('%Y-%m-%d %H:%M:%S')
        rental_date_formatted = rental_date.strftime('%Y-%m-%d %H:%M:%S')

        ret = None
        if not returned:
            ret = 0
        else:
            ret = 1
        data = [(user_id, book_id, rental_date_formatted, return_date, ret), ]
        query = """insert into rentals (user_id, book_id, rental_date, return_date, returned) values (?, ?, ?, ?, ?)"""

        insert_into_database(conn, query, data)

    def send_reminder(self):
        logging.info('Reminder send for {}'.format(self.user.name))
