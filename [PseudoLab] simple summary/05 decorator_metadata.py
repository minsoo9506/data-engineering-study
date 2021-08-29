def double_args(func):
    def wrapper(a, b):
        """This is wrapper
        """
        return func(a * 2, b * 2)
    return wrapper

def multiply(a, b):
    return a * b

@double_args
def multiply(a, b):
    """This is decorated function
    """
    return a * b

# metadata를 살펴보자
print(multiply.__name__) # wrapper
print(multiply.__doc__)  # This is wrapper

# 위에서 우리가 원하는 결과와 다르게 나온다
# 이는 사실 당연한 결과인데 return wrapper을 하기 때문
# 이를 해결하기 위해서 `functools`의 `wraps`를 이용하면 된다

from functools import wraps

def double_args(func):
    @wraps(func)
    def wrapper(a, b):
        """This is wrapper
        """
        return func(a * 2, b * 2)
    return wrapper

def multiply(a, b):
    return a * b

@double_args
def multiply(a, b):
    """This is decorated function
    """
    return a * b

# metadata를 살펴보자
print(multiply.__name__)    # multipy
print(multiply.__doc__)     # This is decorated function

print(multiply.__wrapped__) # <function multiply at 0x0000024FA6FB91F0>