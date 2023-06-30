class MyContextManager:

    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.my_file = None

    def __enter__(self):
        self.my_file = open(self.file_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.my_file.close()


with MyContextManager('email_reminder/' + 'test.txt') as file:
    for line in file.my_file:
        print(line)
