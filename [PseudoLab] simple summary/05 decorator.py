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