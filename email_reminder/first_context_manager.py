class MyContextManager:

    def __init__(self) -> None:
        print('In init')

    def __enter__(self):
        print('In enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('In exit')


with MyContextManager() as my_context:
    print('do job')
