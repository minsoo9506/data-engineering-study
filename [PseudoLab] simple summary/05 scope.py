# nonlocal
x = 10

def out_func(x):
    def in_func():
        x = 100
        return x
    in_func()
    return x

print(out_func(10)) # 10

def out_func(x):
    def in_func():
        nonlocal x
        x = 100
        return x
    in_func()
    return x

print(out_func(10)) # 100 : 바뀜

# global
global_var = 100

def no_change_global():
    global_var = 10
    print(global_var)

def change_global():
    global global_var
    global_var = 10
    print(global_var)

no_change_global() # 10
print(global_var)  # 100
change_global()    # 10
print(global_var)  # 10 : 바뀜