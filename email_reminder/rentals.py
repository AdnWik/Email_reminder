import datetime
import logging

class Rental:
    CURRENT_DATE = datetime.datetime.now()

    def __init__(self, user, book, rental_date, days_of_rental=14) -> None:
        self.user = user
        self.book = book
        self.rental_date = datetime.datetime(rental_date)
        self.days_of_rental = days_of_rental
        self.return_date = datetime.timedelta(self.rental_date,
                                              days=self.days_of_rental)
        self.returned = False

    def send_reminder(self):
        logging.info('Reminder send for {}'.format(self.user.name))
