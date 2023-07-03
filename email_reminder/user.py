from db_conn import create_connection, insert_into_database

class User:

    def __init__(self, user_id, first_name, last_name, email_address) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.name = self.first_name + ' ' + self.last_name
        self.email_address = email_address

    def __repr__(self) -> str:
        return f'{self.name} -> {self.email_address}'

    def __str__(self) -> str:
        return f'{self.name} -> {self.email_address}'

    @staticmethod
    def add_user(conn, first_name, last_name, email_address):
        query = """insert into users (first_name, last_name, email_address) values(?,?,?)"""
        data = [(first_name, last_name, email_address), ]
        insert_into_database(conn, query, data)