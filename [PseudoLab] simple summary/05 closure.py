x = 10

def func1(value):
    def func2():
        print(value)
    return func2

x = 10
my_func = func1(x)
my_func() # 10

del(x)
my_func() # x 지워도 10 나온다
print(len(my_func.__closure__)) # 1
print(my_func.__closure__[0].cell_contents) # 10