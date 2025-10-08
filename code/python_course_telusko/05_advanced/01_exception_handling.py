# Exception handling demo
def divide(a,b):
    try: return a/b
    except ZeroDivisionError: print("Cannot divide by zero"); return None
print(divide(10,2))
print(divide(5,0))
