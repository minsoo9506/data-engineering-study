## Best Practices
### Docstrings
- 여러개 format 존재
  - Google style, numpydoc
- `print(function_name.__doc__)`하면 볼 수 있다

```python
# google
def function_name(arg):
    """Desctiption of what the function does.

    Args:
        arg (str) : ~

    Returns:
        int: ~
    """
# numpydoc
def function_name(arg):
    """
    Desctiption of what the function does.

    Parameters
    ----------
    arg : ~

    Returns
    -------
    The type of the return value
    """
```
### DRY and "Do One Thing"
- Don't repeat yourself
  - 반복되는 코드는 함수화
- Do one thing
  - 함수를 작게 나누기
- 그러면 flexible, debug, change, understand 모두 좋다

### pass by assignment
- 함수의 arg로 넣을 때
  - list같은 것을 넣는 경우 함수내에서 수정하면 수정된다 (mutable)
  - int같은 경우는 그대로다. (immutable)
  - arg에 넣는 값이 참조하는 것이 무엇인지 생각
- 따라서 mutable default argument는 조심

## Context Managers
### Using context managers
- context manager가 왜 필요?
  - 사용한 리소스를 종료
- 아래코드에서 `with`로 시작하고 `open`이  context manager 역할
- `with`가 감싸는 context를 manage
- `with`가 끝나면 `file`은 자동으로 닫아짐
```python
# Open "alice.txt" and assign the file to "file"
with open('alice.txt') as file:
  text = file.read()

n = 0
for word in text.split():
  if word.lower() in ['cat', 'cats']:
    n += 1

print('Lewis Carroll uses the word "cat" {} times'.format(n))
```
### writing context managers
- context manager를 만드는 방법은
  - class-based
  - function-based
- function-based
  - 1. Define a function
  - 2. Add any set up code your context needs
  - 3. Use the `yeild` keyword
  - 4. Add any teardown code your context needs
  - 5. Add the `@contextlib.contextmanger` decorator

```python
@contextlib.contextmanager
def open_read_only(filename):
  """Open a file in read-only mode.

  Args:
    filename (str): The location of the file to read

  Yields:
    file object
  """
  read_only_file = open(filename, mode='r')
  # Yield read_only_file so it can be assigned to my_file
  yield read_only_file
  # Close read_only_file
  read_only_file.close()

with open_read_only('my_file.txt') as my_file:
  print(my_file.read())
```

### Advanced topics
- Nested context
  - 말그대로 nested context를 이용하여 효율적으로 context manage
- Handling error
  - 예를 들어, disconnect를 하기 전에 에러가 발생하면 그 위의 코드는 다 실행된 상태이기 때문에 disconnect를 하지 않고 context가 끝나버린다

```python
def get_db(dbname):
  p = connect_to_db(dbname)
  # do something ~
  try:
    yield
  finally:
    p.disconnect()
```

## Decorators

### Functions are objects
- Python에서는 함수도 일급객체 (해당 언어 내에서 일반적으로 다른 모든 개체에 통용가능한 동작이 지원되는 개체를 의미)
  - 함수의 인자로 전달
  - 함수의 반환값이 되거나
  - 수정되고 할당할 수 있는 것들 등등
- 함수는 list에도 넣을 수 있고
- 변수에 할당해서 사용할 수도 있고
- 함수안에 함수를 넣을 수도 있고
- 여타 다른 object와 동일하다!

```python
def my_function():
  print('Hi')

my_list = [1, 2, my_function]

x = my_function
x() # Hi
```

### Scope
- 함수를 사용할 때, scope 주의!
  - Local, NonLocal, Global, BuiltIn
  - `05 scope.py` 참고

### Closure
- 자신을 둘러싼 scope의 상태값을 기억하는 함수
- 어떤 함수가 closure이기 위해서는?
  - 해당 함수는 어떤 함수의 중첩된 함수
  - 해당 함수는 자신을 둘러싼 함수 내의 상태값을 참조
  - 해당 함수를 둘러싼 함수는 이 함수를 반환
- 아래 코드 참고
  - `func2`는 `func1`에 nested된 함수
  - `func2`는 `func1`내의 상태값 `value`를 참조
  - `func2`를 둘러싼 `func1`은 `func2`를 반환
```python
x = 10

def func1(value):
    def func2():
        print(value)
    return func2

x = 10
my_func = func1(x)
my_func() # 10

del(x)
my_func() # x 지워도 10 나온다!
print(len(my_func.__closure__)) # 1
print(my_func.__closure__[0].cell_contents) # 10
```

### Decorator
- 함수를 감싸고 있다
- 함수를 인자로 받는다

```python
def double_args(func):
    def wrapper(a, b):
        return func(a * 2, b * 2)
    return wrapper

def multiply(a, b):
    return a * b

print(multiply(1, 2)) # 2

new_multiply = double_args(multiply)
print(new_multiply(1, 2)) # 8

# decorator 이용
# 위의 과정과 동일한 과정 진행
# syntax sugar 일뿐

@double_args
def multiply(a, b):
    return a * b

print(multiply(1, 2)) # 8
```
## More on Decorators
- 언제 사용?
  - 함수들에게 공통적인 내용을 추가하고 싶을 때!
  - `05 decorator_ex.py` 참고

### Decorators and metadata
- 위에서처럼 decorator를 사용하면 metadata를 사용할 때 문제가 발생한다
- 아래의 코드를 보면
  - 첫 부분에서는 우리가 원하는 결과와 다르게 나온다
  - 이는 사실 당연한 결과인데 return wrapper을 하기 때문
  - 이를 해결하기 위해서 `functools`의 `wraps`를 이용하면 된다
  - `@wraps(func)`로 `wrapper`함수를 감싼다

```python
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
print(multiply.__name__) # multipy
print(multiply.__doc__)  # This is decorated function
```

### Decorators that take arguments
- decorator가 arg가 필요한 경우가 있다
- 이럴때는 decorator함수를 구현하는 것에서 그치는 것이 아니라 이를 return하는 함수를 만들어야한다

```python
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
```