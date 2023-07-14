import email
import smtplib


class EmailSender:

    def __init__(self, port, smtp_address, credentials) -> None:
        self.port = port
        self.smtp_address = smtp_address
        self.credentials = credentials
        self.connection = None

    def __enter__(self):
        self.connection = smtplib.SMTP(self.smtp_address, self.port)
        self.connection.login(self.credentials.username,
                              self.credentials.password)
        return self

    def send_email(self, sender, receiver, subject, message):
        message = email.message_from_string(message)
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject
        message.set_charset('utf-8')
        self.connection.sendmail(sender, receiver, message.as_string())

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
