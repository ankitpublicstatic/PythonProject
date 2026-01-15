#
# for i in range(10):
#     print(i)
#
# table_name = int( input('Enter table name: '))
#
# for v in range(1, 11):
#     print(table_name," x ",v," = ", table_name * v)
#

def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_decorator
def process_data():
    print("Processing...")

process_data()

def uppercase_decorator(func):
    def wrapper(*args, **kwargs):
        return "hello ankit".upper()
    return wrapper



@uppercase_decorator
def greet_upper():
    return "not used"

def lowercase_decorator(func):
    def wrapper(*args, **kwargs):
        return "hello ankit".lower()
    return wrapper

@lowercase_decorator
def greet():
    # original function body is ignored
    return "Not Used"

# Using the decorator
print("Lowercase:", greet())          # hello world
print("Uppercase:", greet().capitalize())  # HELLO WORLD

num = 7
print("ankit",num)