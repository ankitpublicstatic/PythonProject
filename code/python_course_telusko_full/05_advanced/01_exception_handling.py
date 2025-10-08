# Exception handling demo
def divide(a,b):
    try:
        result = a/b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        result=None
    except Exception as e:
        print("Unexpected error:",e)
        result=None
    else:
        print("Division successful")
    finally:
        print("Execution finished")
    return result

print(divide(10,2))
print(divide(5,0))
