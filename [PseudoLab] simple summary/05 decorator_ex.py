# 함수가 작동하는 시간 파악
import time

def timer(func):
    def wrapper(*args, **kwargs):
        t_start = time.time()
        result = func(*args, **kwargs)
        t_end = time.time()
        total_time = t_end - t_start
        print(f'{func.__name__}함수는 {total_time:.3f}초 걸린다.')
        return result
    return wrapper

@timer
def func1():
    time.sleep(1)
    return 'Hi'

@timer
def func2():
    time.sleep(2)
    return 'Hello'

func1() # func1함수는 1.010초 걸린다.
func2() # func2함수는 2.004초 걸린다.

# ------------------------------------------- #
# memoize

def memoize(func):
    cache = {}
    def wrapper(*args, **kwargs):
        if (args, kwargs) not in cache:
            cache[(args, kwargs)] = func(*args, **kwargs)
        return cache[(args, kwargs)]
    return wrapper

@memoize
def slow_func(a, b):
    time.sleep(2)
    print(a + b)
    return a + b

slow_func(1,2) # 2초 뒤에 3
slow_func(1,2) # 바로 3 : cache 이용