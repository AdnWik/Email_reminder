class Book:

    def __init__(self, book_id, title, author, created_at) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.created_at = created_at

    def __repr__(self) -> str:
        return f'{self.title} - {self.author}'

    def __str__(self) -> str:
        return f'{self.title} - {self.author}'
