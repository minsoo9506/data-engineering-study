def run_n_times(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@run_n_times(3)
def print_sum(a, b):
    print(a + b)

@run_n_times(2)
def print_hello():
    print('Hello')

print_sum(1,2) # 3이 3번 나옴
print_hello()  # Hello가 2번 나옴