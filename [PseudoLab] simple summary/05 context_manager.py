import contextlib

@contextlib.contextmanager
def my_context():
    print('Hello')
    yield 'minsoo'
    print('Bye')

with my_context() as name:
    print(f'I\'m {name}')

# Hello
# I'm minsoo
# Bye